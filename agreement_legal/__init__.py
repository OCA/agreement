# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from . import models
from . import wizards


def uninstall_hook(env):
    menu_root = env.ref("agreement.agreement_menu_root", raise_if_not_found=False)
    if menu_root:
        menu_root.active = True
