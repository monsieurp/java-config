#!/usr/bin/python -E
# -*- coding: UTF-8 -*-

# Copyright 2004-2006 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

from java_config_2 import __version__
from java_config_2.OutputFormatter import OutputFormatter
from java_config_2.EnvironmentManager import EnvironmentManager
from java_config_2.Errors import *

#import os
import sys

#global printer, manager
printer = OutputFormatter(True, True)
manager = EnvironmentManager()
#try:
#    # Python 3.
#    from subprocess import getoutput
#except ImportError:
#    # Python 2.
#    from commands import getoutput
#
#from optparse import OptionParser, make_option
#
#def version(option, opt, value, parser):
#    printer._print("%H%BJava Configuration Utility %GVersion " + str(__version__))
#    raise SystemExit()
#
#def nocolor(option, opt, value, parser):
#    printer.setColorOutputStatus(False)
#
#def get_command(command):
#    try:
#        printer._print(manager.get_active_vm().find_exec(command))
#    except PermissionError:
#        fatalError("The " + command + " executable was not found in the Java path")
#
#def java(option, opt, value, parser):
#    get_command('java')
#
#def javac(option, opt, value, parser):
#    get_command('javac')
#
#def jar(option, opt, value, parser):
#    get_command('jar')
#
#def query_active_vm(var):
#    try:
#        printer._print(manager.get_active_vm().query(var))
#    except EnvironmentUndefinedError:
#        fatalError("%s could not be found in the active VM environment" % var)
#
#def query_active_vm_cb(option, opt, value, parse, *args):
#    return query_active_vm(args[0])
#
#def tools(option, opt, value, parser):
#    jh = ''
#    try:
#        jh = manager.get_active_vm().query('JAVA_HOME')
#    except EnvironmentUndefinedError:
#        fatalError("JAVA_HOME not found in the active VM environment")
#    tools_jar = jh + '/lib/tools.jar'
#    if os.path.exists(tools_jar):
#        printer._print(tools_jar)
#    else:
#        sys.exit(1);
#
#def show_active_vm(option, opt, value, parser):
#    printer._print(manager.get_active_vm().name())
#
#def java_version(option, opt, value, parser):
#    try:
#        printer._print(getoutput('%s -version' % manager.get_active_vm().find_exec('java')))
#    except PermissionError:
#        fatalError("The java executable was not found in the Java path")
#
#def query_pkg_path(option, opt, value, parser, query):
#    error = False
#    try:
#        packages = value.split(',')
#        path = set()
#        missing_deps = set()
#        if not parser.values.with_deps:
#            path = manager.build_path(packages, query)
#        else:
#            path = manager.build_dep_path(packages, query, missing_deps)
#
#        printer._print(':'.join(path))
#
#        if len(missing_deps) > 0:
#            for dep in missing_deps:
#                printer._printError("Dependency package %s was not found!" % dep)
#            error = True
#
#    except UnexistingPackageError, e:
#        printer._printError("Package %s was not found!" % e.package)
#        error = True
#
#    if error:
#        sys.exit(1)
#
def query_pkg(option, opt, value, parser ,query=None):
    error = False
    if query: pass
    else:
        query = parser.values.query
    if query:
        try:
            package = manager.get_package(value)
            if package.query(query):
                result=package.query(query)
                printer._print(package.query(query))
                return result
            else:
                printer._printError('Package %s does not define %s in it\'s package.env.' % (package.name(), query))
        #change to can be compiled both in Python 2.5 and 3.1
        #except UnexistingPackageError, e:
        except UnexistingPackageError:
            e, e_info, e_traceback=sys.exc_info()
            printer._printError("Package %s was not found!" % e.package)
            error = True
        except PermissionError:
            printer._printError("You do not have enough permissions to read the package's package.env")
            error = True
    else:
        printer._printError("No query parameter was specified, unable to retrieve package.env value.")
        error = True

    if error:
        sys.exit(1)
#
#def get_virtual_providers( option, opt, value, parser):
#    if manager.get_virtual(value):
#        output = manager.get_virtual(value).get_packages()
#        printer._print(','.join(output))
#    else:
#        printer._printError("Virtual package %s was not found" % value)
#        sys.exit(1)
#
#def get_env(option, opt, value, parser):
#    for env in value.split(','):
#        query_active_vm(env)
#
#def exec_cmd(option, opt, value, parser):
#    for cmd in iter(value.split(',')):
#        os.system(cmd)

def list_available_packages(option, opt, value, parser):
    for package in manager.get_packages().values():
        printer._print("[%s] %s (%s)" % (package.name(), package.description(), package.file()))

#def list_available_vms(option, opt, value, parser):
#    vm_list = manager.get_virtual_machines()
#    try:
#        active = manager.get_active_vm()
#    except InvalidVMError:
#        active = None
#
#    found_build_only = False
#    printer._print('%HThe following VMs are available for generation-2:%$')
#    for i, vm in vm_list.items():
#        if vm is active:
#            if not vm.is_build_only():
#                printer._print('%G' + '*)\t%s [%s]%s' % (vm.query('VERSION'), vm.name(), '%$'))
#            else:
#                printer._print('%G' + '*)\t%s [%s]%s' % (vm.query('VERSION'), vm.name(), '%$') + '%r (Build Only)%$')
#                found_build_only = True
#        else:
#            if not vm.is_build_only():
#                printer._print('%i)\t%s [%s]' % (i, vm.query('VERSION'), vm.name()))
#            else:
#                printer._print('%i)\t%s [%s]' % (i, vm.query('VERSION'), vm.name()) + '%r (Build Only)%$')
#                found_build_only = True
#
#    if (found_build_only):
#        printer._print('')
#        printer._print('%r' + 'VMs marked as Build Only may contain Security Vulnerabilities and/or be EOL.')
#        printer._print('%r' + 'Gentoo recommends not setting these VMs as either your System or User VM.')
#        printer._print('%r' + 'Please see http://www.gentoo.org/doc/en/java.xml#build-only for more information')
#
#def print_environment(option, opt, value, parser):
#    vm = manager.get_vm(value) 
#    if vm:
#        manager.create_env_entry(vm, printer, "%s=%s")
#    else:
#        fatalError("Could not find a vm matching: %s" % value)
#
#def set_system_vm(option, opt, value, parser):
#    vm = manager.get_vm(value)
#
#    if not vm:
#        fatalError("Could not find a vm matching: %s" % value)
#    else:
#        if os.getuid() is 0:
#            try:
#                manager.set_system_vm(vm)
#                printer._print("Now using %s as your generation-2 system JVM" % (vm) )
#                if vm.is_build_only():
#                    printer._printWarning("%s is marked as a build-only JVM. Using this vm is not recommended. " % (vm))
#                    printer._printWarning("Please see http://www.gentoo.org/doc/en/java.xml#build-only for more information.")
#            except PermissionError:
#                fatalError("You do not have enough permissions to set the system VM!")
#            except EnvironmentUndefinedError:
#                fatalError("The selected VM is missing critical environment variables.")
#            except InvalidConfigError, e:
#                fatalError("Target file already exists and is not a symlink: %s" % e.file)
#        else:
#            fatalError("You do not have enough permissions to set the system VM!")
#
#def set_user_vm(option, opt, value, parser):
#    vm = manager.get_vm(value)
#
#    if not vm:
#        fatalError("Could not find a vm matching: %s" % value)
#    else:
#        if os.getuid() is 0:
#            fatalError("The user 'root' should always use the System VM")
#        else:
#            try:
#                manager.set_user_vm(vm)
#                printer._print("Now using %s as your user JVM" % (vm))
#                if vm.is_build_only():
#                    printer._printWarning("%s is marked as a build-only JVM. Using this vm is not recommended. " % (vm))
#                    printer._printWarning("Please see http://www.gentoo.org/doc/en/java.xml#build-only for more information.")
#            except PermissionError:
#                fatalError("You do not have enough permissions to set the VM!")
#            except InvalidConfigError, e:
#                fatalError("Target file already exists and is not a symlink: %s" % e.file)
#
## Deprecated
#def system_classpath_target():
#    # TODO: MAKE THIS MODULAR!! (compnerd)
#    return [{'file': '/etc/env.d/21java-classpath', 'format': '%s=%s\n' }]
#
#def user_classpath_target():
#    # TODO: MAKE THIS MODULAR!! (compnerd)
#    return [
#            {'file': os.path.join(os.environ.get("HOME"), '.gentoo/java-env-classpath'),     'format': 'export %s=%s\n' },
#            {'file': os.path.join(os.environ.get("HOME"), '.gentoo/java-env-classpath.csh'), 'format': 'setenv %s %s\n' }
#        ]
## Deprecated
#def set_system_classpath(option, opt, value, parser):
#    deprecation_notice()
#    if os.getuid() is 0:
#        pkgs = value.split(',')
#        manager.set_classpath(system_classpath_target(), pkgs)
#        
#        for package in pkgs:
#            printer._printError("Package %s was not found!" % package)
#            
#        update_env()
#    else:
#       fatalError("You do not have enough permissions to set the system classpath!")
#
## Deprecated
#def set_user_classpath(option, opt, value, parser):
#    deprecation_notice()
#    pkgs = value.split(',')
#    manager.set_classpath(user_classpath_target(), pkgs)
#
#    for package in pkgs:
#        printer._printError("Package %s was not found!" % package)
#
#    user_update_env()
#
## Deprecated
#def append_system_classpath(option, opt, value, parser):
#    deprecation_notice()
#    if os.getuid() is 0:
#        pkgs = value.split(',')
#        manager.append_classpath(system_classpath_target(), pkgs)
#
#        for package in pkgs:
#            printer._printError("Package %s was not found!" % package)
#
#        update_env()
#    else:
#        fatalError("You do not have enough permissioins to append to the system classpath!")
#
## Deprecated
#def append_user_classpath(option, opt, value, parser):
#    deprecation_notice()
#    pkgs = value.split(',')
#    manager.append_classpath(user_classpath_target(),  pkgs)
#
#    for package in pkgs:
#        printer._printError("Package %s was not found!" % package)
#
#    user_update_env()
#
## Deprecated
#def clean_system_classpath(option, opt, value, parser):
#    deprecation_notice()
#    if os.getuid() is 0:
#        manager.clean_classpath(system_classpath_target())
#        update_env()
#    else:
#        fatalError("You do not have enough permissions to clean the system classpath!")
#
## Deprecated
#def clean_user_classpath(option, opt, value, parser):
#    deprecation_notice()
#    manager.clean_classpath(user_classpath_target())
#
#def select_vm(option, opt, value, parser):
#    if value == '':
#        return
#
#    vm = manager.get_vm(value)
#    if vm:
#        manager.set_active_vm(manager.get_vm(value))
#    else:
#        fatalError("The vm could not be found")
#
#def update_env():
#    printer._print(getoutput("/usr/sbin/env-update"))
#    printer._printAlert("If you want the changes too take effect in your current session, you should update\n\
#            your environment by running: source /etc/profile")
#
#def user_update_env():
#    printer._printAlert("Environment files in ~/.gentoo/ have been updated. You should source these from your shell's profile.\n\
#            If you want the changes too take effect in your current sessiosn, you should resource these files")
#
#def deprecation_notice():
#    printer._printWarning("Setting a user and system classpath is deprecated, this option will be removed from future versions.")
#
#def fatalError(msg):
#    printer._printError(msg)
#    sys.exit(1)
#
#if __name__ == '__main__':
#
#    usage =  "java-config [options]\n\n"
#    usage += "Java Configuration Utility Version " + str(__version__) + "\n"
#    usage += "Copyright 2004-2005 Gentoo Foundation\n"
#    usage += "Distributed under the terms of the GNU General Public License v2\n"
#    usage += "Please contact the Gentoo Java Herd <java@gentoo.org> with problems."
#
#    options_list = [
#                     make_option ("-V", "--version",                action="callback", callback=version,                help="Print version information"),
#                     make_option ("-n", "--nocolor",                action="callback", callback=nocolor,                help="Disable color output"),
#                     make_option (""  , "--select-vm",              action="callback", callback=select_vm,              help="Use this vm instead of the active vm when returning information",                     type="string", dest="vm"),
#                     make_option ("-J", "--java",                   action="callback", callback=java,                   help="Print the location of the java executable"),
#                     make_option ("-c", "--javac",                  action="callback", callback=javac,                  help="Print the location of the javac executable"),
#                     make_option ("-j", "--jar",                    action="callback", callback=jar,                    help="Print the location of the jar executable"),
#                     make_option ("-t", "--tools",                  action="callback", callback=tools,                  help="Print the path to tools.jar"),
#                     make_option ("-f", "--show-active-vm",         action="callback", callback=show_active_vm,         help="Print the active Virtual Machine"),
#                     make_option ("-v", "--java-version",           action="callback", callback=java_version,           help="Print version information for the active VM"),
#                     make_option ("-g", "--get-env",                action="callback", callback=get_env,                help="Print an environment variable from the active VM",                                    type="string", dest="var"),
#                     make_option ("-P", "--print",                  action="callback", callback=print_environment,      help="Print the environment for the specified VM",                                          type="string", dest="vm"),
#                     make_option ("-e", "--exec_cmd",               action="callback", callback=exec_cmd,               help="Execute something which is in JAVA_HOME",                                             type="string", dest="command"),
#                     make_option ("-L", "--list-available-vms",     action="callback", callback=list_available_vms,     help="List available Java Virtual Machines"),
#                     make_option ("-S", "--set-system-vm",          action="callback", callback=set_system_vm,          help="Set the default Java VM for the system",                                              type="string", dest="vm"),
#                     make_option ("-s", "--set-user-vm",            action="callback", callback=set_user_vm,            help="Set the default Java VM for the user",                                                type="string", dest="vm"),
#                     make_option ("-l", "--list-available-packages",action="callback", callback=list_available_packages,help="List all available packages on the system."),
#                     make_option ("-d", "--with-dependencies",      action="store_true",                                help="Include package dependencies in --classpath and --library calls",                     default=False, dest="with_deps"),
#                     make_option ("-p", "--classpath",              action="callback", callback=query_pkg_path,         help="Print entries in the environment classpath for these packages",                       type="string", dest="package(s)", callback_args = ("CLASSPATH",)),
#                     make_option ("",   "--package",                action="callback", callback=query_pkg,              help="Retrieve a value from a packages package.env file, value is specified by --query",    type="string", dest="package(s)"),
#                     make_option ("-D", "--javadoc",                action="callback", callback=query_pkg,              help="Retrieve java doc's path of specific package",                                       type="string", dest="package(s)", callback_args = ("JAVADOC_PATH",)),
#                     make_option ("-C", "--src",                    action="callback", callback=query_pkg,              help="Retrieve java source's path of specific package",                                       type="string", dest="package(s)", callback_args = ("JAVA_SOURCES",)),
#                     make_option ("-q", "--query",                  action="store",                                     help="Value to retieve from packages package.env file, specified by --package",             type="string", dest="query"),
#                     make_option ("-i", "--library",                action="callback", callback=query_pkg_path,         help="Print java library paths for these packages",                                         type="string", dest="package(s)", callback_args = ("LIBRARY_PATH",)),
#                     make_option ("-A", "--set-system-classpath",   action="callback", callback=set_system_classpath,   help="(Deprecated) Set the system classpath to include the libraries",                      type="string", dest="package(s)" ),
#                     make_option ("-B", "--append-system-classpath",action="callback", callback=append_system_classpath,help="(Deprecated) Append the libraries to the system classpath",                           type="string", dest="package(s)"),
#                     make_option ("-X", "--clean-system-classpath", action="callback", callback=clean_system_classpath, help="(Deprecated) Clean the current system classpath"),
#                     make_option ("-a", "--set-user-classpath",     action="callback", callback=set_user_classpath,     help="(Deprecated) Set the user classpath to include the libraries",                        type="string", dest="package(s)"),
#                     make_option ("-b", "--append-user-classpath",  action="callback", callback=append_user_classpath,  help="(Deprecated) Append the libraries to the user classpath",                             type="string", dest="package(s)"),
#                     make_option ("-x", "--clean-user-classpath",   action="callback", callback=clean_user_classpath,   help="(Deprecated) Clean the current user classpath"),
#                     make_option ("",   "--get-virtual-providers",  action="callback", callback=get_virtual_providers,  help="(Experimental) Return a list of packages that provide a virtual",                     type="string", dest="package(s)"),
#                     make_option ("-r", "--runtime",                action="callback", help="Print the runtime classpath",
#                                     callback=query_active_vm_cb, callback_args=("BOOTCLASSPATH",)),
#                     make_option ("-O", "--jdk-home",               action="callback", help="Print the location of the active JAVA_HOME",
#                                     callback=query_active_vm_cb, callback_args=("JAVA_HOME",)),
#                     make_option ("-o", "--jre-home",               action="callback", help="Print the location of the active JAVA_HOME",
#                                     callback=query_active_vm_cb, callback_args=("JAVA_HOME",))
#                   ]
#
#    parser = OptionParser(usage, options_list)
#
#    if len(sys.argv) < 2: 
#        parser.print_help()
#    else:
#        try:
#            # Makes sure that --nocolor and --query are always 
#            # the first argument(s)
#            # because otherwise callbacks before it will output
#            # colored output or --query param will not be set for
#            # the query_pkg callback
#
#            args = sys.argv[1:]
#            for opt in ('-q', '--query'):
#                try:
#                    args.remove(opt)
#                    args.insert(0, opt)
#                except ValueError:
#                    pass
#            args = sys.argv[1:]
#            for opt in ( '-n', '--nocolor'):
#                try:
#                    args.remove(opt)
#                    args.insert(0,opt)
#                except ValueError:
#                    pass
#
#            (options, args) = parser.parse_args(args=args)
#        except InvalidVMError:
#            fatalError("The active vm could not be found")
#        except ProviderUnavailableError, e:
#            message = "No providers are available, please ensure you have one of the following VM's or Package's;\n"
#            message += "VM's (Your active vm must be one of these): " + e.vms() + "\n"
#            message += "Packages's: " + e.packages() + "\n"
#            fatalError(message)

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap: