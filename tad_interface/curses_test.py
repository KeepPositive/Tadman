import curses
import curses_main
S_DICT = {'Enable verbose build': ['--enable-verbose', 'Output extra info while configuring'],
          'Enable unicode support': ['--enable-unicode', 'UTF-8 is the true master race!'],
          'Disable squid mode': ['--disable-squid', 'What does this do?'],
          'Disable colored output': ['--disable-color', 'Disable color for those that are colorblind'],
          'Use old legacy driver': ['--enable-legacy-driver', 'For lovers of classic Linux 2.4']
        }
L_DICT = {'Enable verbose build': ['--enable-verbose', 'Output extra info while configuring'],
          'Enable unicode support': ['--enable-unicode', 'UTF-8 is the true master race!'],
          'Disable squid mode': ['--disable-squid', 'What does this do?'],
          'Disable colored output': ['--disable-color', 'Disable color for those that are colorblind'],
          'Use old legacy driver': ['--enable-legacy-driver', 'For lovers of classic Linux 2.4'],
          'Disable Option Checking': ['--disable-option-checking', 'Ignore unrecognized --enable/--with options'],
          'Disable Feature': ['--disable-FEATURE', 'Do not include feature (same as --enable-feature=no)'],
          'Enable Feature[=Arg]': ['--enable-FEATURE[=ARG]', 'Include feature [arg=yes]'],
          'Enable Silent Rules': ['--enable-silent-rules', "Less verbose build output (undo: `make v=1')"],
          'Disable Silent Rules': ['--disable-silent-rules', "Verbose build output (undo: `make v=0')"],
          'Enable Strict Ansi': ['--enable-strict-ansi', 'Enable strict ansi compliance build [[default=no]]'],
          'Enable Super Warnings': ['--enable-super-warnings', 'Enable extra compiler warnings [[default=no]]'],
          'Enable Debug': ['--enable-debug', 'Build a debug version [[default=no]]'],
          'Enable Gprof': ['--enable-gprof', 'Enable gprof profiling output [[default=no]]'],
          'Enable Gprof Libc': ['--enable-gprof-libc', 'Link against libc with profiling support [[default=no]]'],
          'Enable Dependency Tracking': ['--enable-dependency-tracking', 'Do not reject slow dependency extractors'],
          'Enable Shared[=Pkgs]': ['--enable-shared[=PKGS]', 'Build shared libraries [default=yes]'],
          'Enable Static[=Pkgs]': ['--enable-static[=PKGS]', 'Build static libraries [default=yes]'],
          'Enable Fast Install[=Pkgs]': ['--enable-fast-install[=PKGS]', 'Optimize for fast installation [default=yes]'],
          'Disable Nls': ['--disable-nls', 'Do not use native language support'],
          'Disable Rpath': ['--disable-rpath', 'Do not hardcode runtime library paths'],
          'Disable Startup Notification': ['--disable-startup-notification', 'Disable the startup notification library. [default=enabled]'],
          'Disable Xcursor': ['--disable-xcursor', 'Disable use of the x cursor library. [default=enabled]'],
          'Disable Xkb': ['--disable-xkb', 'Build without support for xkb extension [default=enabled]'],
          'Disable Xsync': ['--disable-xsync', 'Build without support for xsync extension [default=enabled]']
         }

N_INTERFACE = curses_main.MainInterface(L_DICT, 'squid', '1.4.18', 'autotools')
N_INTERFACE.init_option_loop()
if N_INTERFACE.run_option_loop():
    print(N_INTERFACE.get_return_values())
else:
    print("Tadman build was canceled")
