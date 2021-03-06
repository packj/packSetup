#!/usr/bin/env python

# When "record" is called:
#    record a macro, display, prompt to confirm/redo, create a unique identifier, store as yaml

# When "play" is called:
#    find yaml file with uid, run it

from Tkinter import *

import os
homedir = os.path.expanduser("~")
outdir = os.path.join(homedir, 'df', 'saved_macros')  #fixme: hardcoded


class Recorder():
    from pynput.keyboard import Key, Listener, Controller
    import time
    
    def __init__(self, stopkey=Key.f5,confirm=1):
        self.reset()
        self.stopkey = stopkey
        self.confirm = confirm
        K = self.Key
        self.modifiers = [K.alt, K.alt_l, K.alt_r, K.ctrl, K.ctrl_l, K.ctrl_r, K.shift, K.shift_l, K.shift_r]
        self.outdir = outdir

    def __call__(self):
        self.go()
        
    def reset(self):
        #initialize our new macro to empty
        self.macro = []
        now = self.time.time()
        self.startTime = now
        self.lasttime = now
        self.aheld = 0
        self.cheld = 0
        self.sheld = 0
        self.started = 0
        self.finished = 0

    def __which_mod(self, key, val):
        if key in self.modifiers:
            if key in [self.Key.shift_l, self.Key.shift_r, self.Key.shift]:
                self.sheld = val
            if key in [self.Key.alt_l, self.Key.alt_r, self.Key.alt]:
                self.aheld = val
            if key in [self.Key.ctrl_l, self.Key.ctrl_r, self.Key.ctrl]:
                self.cheld = val
        
    def __on_press(self, key):
        if key in self.modifiers:
            self.__which_mod(key, 1)
            return
        if key == self.stopkey:
            if self.started:
                self.finished = 1
            else:
                self.started = 1
                self.lb.configure(bg='green', text='Recording macro now... press F5 to stop')
        else:
            if self.started:
                now = self.time.time()
                t = now - self.lasttime
                self.lasttime = now
                import active
                aw = str(active.get_active_window())
                to_add = [[self.aheld+2*self.cheld+4*self.sheld, key], t, aw]
                self.macro.append(to_add)
        print '.'
            
    def __on_release(self, key):
        if key in self.modifiers:
            self.__which_mod(key, 0)
            return

    def __write(self):
        import yaml, os
        filename = os.path.join(self.outdir, self.uid)
        print filename
        out = {}
        out['tags'] = self.tags
        out['macro'] = self.macro
        with open(filename,'w') as f:
            yaml.dump(out, f)
            print 'oy'
                
    def __confirm(self):
        # display the recorded macro and a default UID
        for e in self.macro:
            print e
        # UID should be editable, there should be an area to add tags
        self.tags = []
        # prompt user: accept, retry, reject
        import time, getpass, socket
        uid_tail = 'user_%s___hostname_%s' % (getpass.getuser(), socket.gethostname())
        self.uid = time.strftime("date_%Y_%m_%d___time_%H_%M_%S___") + uid_tail
        print 'UID has been autogenerated: %s' % self.uid
        print 'Please select one:'
        print '   [1] Accept'
        print '   [2] Retry'
        print '   [3] Reject'
        while 1:
            sel = raw_input()
            # if accept, return 1
            # if retry, call go, then return 0
            # if reject, return 0
            if sel == '1':
                return 1
            if sel == '2':
                self.reset()
                self.go()
                return 0
            if sel == '3':
                return 0
            print 'Unrecognized choice...please try again'
            
    def go(self):    
        #listen to all input and wait for the stopkey
        
        tk = Tk()
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        Nx  = 250
        Ny = 150
        tk.geometry("%dx%d+%d+%d" % (Nx, Ny, screen_width-Nx, 0))
        tk.configure(background='gold')
        tk.overrideredirect(1)
        self.lb = Label(tk, text="Press F5 to start recording macro", wraplength=Nx, font=('Arial',16), background='gold', anchor='center')
        self.lb.pack(fill=BOTH, expand=1)
        tk.lift()
            

        with self.Listener(
                on_press=self.__on_press,
                on_release=self.__on_release) as listener:
            
            while 1:
                self.time.sleep(0.01)
                tk.update()
                if self.finished:
                    break

        listener.stop()
        tk.destroy()

        if self.__confirm():
            self.__write()

class Player():
    from pynput.keyboard import Key
    def __init__(self, uid, speed=1, startkey=Key.f5):
        self.outdir = outdir
        self.uid = uid
        self.speed = speed
        self.startkey=startkey
        
    def __on_press(self, key):
        pass

    def __on_release(self, key):
        if key == self.startkey:
            self.finished = 1

    def __get_mods(self, code):
        keys = []
        K = self.Key
        if code & 4:
            keys.append(K.shift_l)
        if code & 2:
            keys.append(K.alt_l)
        if code & 1:
            keys.append(K.ctrl_l)
        return keys
    
    def __call__(self):
        import yaml, os, time
        filename = os.path.join(self.outdir, self.uid)
        if os.path.isfile(filename):
            with open(filename) as f:
                yin=yaml.load(f, Loader=yaml.FullLoader)

        # wait for user to press F5
        tk = Tk()
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        Nx  = 250
        Ny = 150
        tk.geometry("%dx%d+%d+%d" % (Nx, Ny, screen_width-Nx, 0))
        tk.configure(background='gold')
        tk.overrideredirect(1)
        self.lb = Label(tk, text="Press F5 to start playing macro", wraplength=Nx, font=('Arial',16), background='gold', anchor='center')
        self.lb.pack(fill=BOTH, expand=1)
        tk.lift()
            

        from pynput.keyboard import Key, Listener, Controller

        self.finished = 0
        with Listener(
                on_press=self.__on_press, on_release=self.__on_release) as listener:
            while 1:
                time.sleep(0.01)
                tk.update()
                if self.finished:
                    break

        listener.stop()
        tk.destroy()

        kb = Controller()
        yin['macro'][0][1] = 0
        for e in yin['macro']:
            time.sleep(e[1]/self.speed)
            mods = self.__get_mods(e[0][0])
            for m in mods:
                kb.press(m)
            kb.press(e[0][1])
            for m in mods:
                kb.release(m)
            #time.sleep(0.01)
            kb.release(e[0][1])

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        r = Recorder()
        r()
    else:
        import glob, os
        flist = glob.glob(os.path.join(outdir, 'date*'))
        f = flist[-1]
        p = Player(f, speed=30)
        p()
    

