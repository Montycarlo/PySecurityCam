#! /usr/bin/python2
#
# Josh Brown
# EPIDEV 2016
#

import curses

class ListWindow:

  def __init__(self, ls, title, wid):
    self.ls = ls
    self.title = title
    self.wid = wid
    self.win = curses.newwin(wid,70)
    self.win.attrset(curses.color_pair(7))
    self.draw()

  def draw(self):
    col = curses.color_pair(0)
    w = self.win

    title = "{0!s:^#080}".format(self.title)
    w.addstr(1,1, title, col)
    w.addstr(2,1, "-"*68, col)
    w.box()

  def refresh(self):
    self.win.refresh()

def run(stdscr):
  curses.use_default_colors()
  for i in range(0, curses.COLORS):
    curses.init_pair(i, i, -1)

  stdscr.attrset(curses.color_pair(1))
  stdscr.addstr(15,2, str(curses.has_colors()), curses.color_pair(0))
  stdscr.box()

  #w1 = curses.newwin(10,20, 0,0)
  #w1.attrset(curses.color_pair(7))
  #w1.border(0, 0, 0, 0)
  ##w1.box()
  #w2 = curses.newwin(10,20, 3,10)
  #w2.attrset(curses.color_pair(7))
  #w2.box()

  stdscr.refresh()

  lw = ListWindow([], "WINDOW TITLE", 80)
  lw.refresh()
  #w1.refresh()
  #w2.refresh()

  while 1:
    pass

curses.wrapper(run)
