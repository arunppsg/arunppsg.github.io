+++
title = "Installing Python Package When Offline"
date = 2026-02-08
tags = ['til', 'python']
+++

Power went down when I was working and I wanted to install a package, which I had installed before but uninstalled recently for testing.

`uv` had a `offline` flag which when set, looks for package in the local instead of searching for the index.

Example: `uv pip install --upgrade textual --offline`
