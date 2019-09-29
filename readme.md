# shlack

[![GitHub Actions status](https://github.com/nolanbconaway/shlack/workflows/Main%20Workflow/badge.svg)](https://github.com/nolanbconaway/shlack/actions)

`shlack` is a command line tool which sends slack messages.

## Quickstart

First, [set up a slack app](#setting-up-a-slack-app) for shlack and have the oauth API token handy.

Then install shlack to your python 2.7, 3.5, 3.6, or 3.7 environment:

``` sh
pip install git+https://github.com/nolanbconaway/shlack.git
```

Export your slack oauth token:

``` sh
$ export SLACK_OAUTH_API_TOKEN='...'
```

Now send yourself a message! shlack will read your token from the variable you exported.

``` sh
$ shlack message 'Hello!' --channel '@nolan'
```

Add an attachment:

``` sh
$ shlack message 'Hello!' -c '@nolan' --attach 'Date' "$(date)"
```

shlack can also send you a notification after a long-running task has completed.

``` sh
$ shlack task 'sleep 10 && echo done' --channel '@nolan'
```

Running that will spin up a process detached from your terminal session, so you can  grab some lunch :-).

Need help? Just ask:

``` sh
$ shlack task --help
```

## shlack is a lot like [jarjar](https://github.com/AusterweilLab/jarjar)

Both are python projects for sending slack messages to your teams. Both have task execution/notification capabilities. But heres whats different:

### shlack requires an app, jarjar uses webhooks

When jarjar was developed, [incoming webhooks](https://my.slack.com/apps/A0F7XDUAZ-incoming-webhooks) were _the_ way to send messages to your team. Nowadays, Slack still supports those webhooks but is pushing users towards replacing them with apps. Apps can access other API features such as user listing, which could be helpful towards solving at least one [bug](https://github.com/AusterweilLab/jarjar/issues/20) in jarjar.

Migrating to apps would result in breaking changes to jarjar's API and would require extensive rewriting of the codebase, hence the decision to develop shlack separately from jarjar.

### shlack ditched the python API

Jarjar included a rich python API; including decorators, jupyter magics, and so on. But at this point there are many great, fully featured slack python APIs. My feeling was that it would be better to lean on one of those rather than implement another (specifically, shlack relies on [slacker](https://github.com/os/slacker)).

### shlack is unit tested

Jarjar performs as expected for most people who use it, but has not been unit tested. We didn't know how to write testable code when developing the package. For reasons outlined below, the code would need extensive changes to implement testing. Making these changes would perpetuate API breakages, hence the decision to implement the shlack tool.

### shlack executes tasks in detached processes rather than screens

This is maybe an obscure point but it involves an important tradeoff:

* [GNU Screens](https://www.gnu.org/software/screen/) have the upside that users can inspect them to check on their processes. But they're impossible to manipulate in pure python as far as I know. For jarjar, we edited some code from [screenutils](https://github.com/Christophe31/screenutils) which wraps common screen manipulations using `subprocess` and `os.system` . It's the first place to look when jarjar performs unexpectedly, it's a nightmare to debug, and it is still a black box to me.
* With detached process, users can't really check in on the process as its running. However, we can execute an arbitrary function in a detached process using pure python! It's still hard to reason about but at least it can be tested straightforwardly.
* An additional benefit is that the user environment is preserved in the a detached process but not in a screen. This resolves a longstanding bug in jarjar when using virtualenvs.

### shlack will not look for special config files

A large segment of jarjar's complexity (and convenience!) comes from the `.jarjar` config files which contain default settings for the module.

shlack reduces complexity (and flexibility!) through a single point of access (command line) and two sources of input: `--options` and environment variables.

## Setting up a Slack App

Start by heading over to the [apps page](https://api.slack.com/apps) and hit the "create new app" button.

Name your app whatever you want (I called mine, `shlack` ) and assign it to your workspace of choice if you have multiple workspaces. Then hit "create app".

Slack should take you to an app management page. Hit the "Permissions" button (or the "OAuth & Permissions" tab on the sidebar).

Scroll down to the "Scopes" section. Add the following two scopes:

1. `chat:write:bot` . Shlack needs this to post messages.
2. `files:write:user` . Shlack does not use this scope at present, but one day will upload the output of more verbose tasks as files rather than as messages.

Hit the "Save Changes" button once those two scopes are selected. Then scroll to the top of the page and hit the "Install App to Workspace" button. Slack will ask you to allow the app to access the scopes you set up.

The page will refresh and at the top you'll find a new OAuth Access Token. Copy that and put it somewhere for later.

Now you can style the app as you see fit :). Hit the "Basic Information" tab at the top of the sidebar and scroll down to the "Display Information" section. Style to your liking. I use this photo which I found by searching "dog with cowboy hat" on the internet.

<p align="center">
  <a href='/img/hero.png'><img src="/img/hero.png" width="200" height="200"></a>
</p>

Then you're done! Enjoy your shlack app.

## Todo

* [ ] Clip very large attachments. Slack will do it automatically but its NOT graceful. Maybe attach as files instead? This is much easier thanks to slacker :-).
* [ ] Write some tooling to help users through errors when their display names are not the same as their usernames. Maybe a command to search users. Maybe just some documentation.
* [ ] Add images in the docs.
* [ ] Add option to enable / disable stdout inclusion in `shlack task` .
* [ ] Surface child PID to user in `shlack task` .

