#!/usr/bin/env python3

import sys
import data

user = sys.argv[1]
repo = sys.argv[2]

print(data.travis(user, repo))
