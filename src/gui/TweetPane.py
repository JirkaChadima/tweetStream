import pygtk
pygtk.require('2.0')
import gtk, pango, gobject

__author__="Jiri Chadima"
__date__ ="$Mar 7, 2011 11:07:05 AM$"

class TweetPane:
    """GTK pane that is showing tweets"""
    def __init__(self):
        """Tree view is set into scrolled view. ListStore is the model."""
        self.scrolled_window = gtk.ScrolledWindow()
        self.model = gtk.ListStore(str, str)
        self.tree_view = gtk.TreeView(self.model)
        self.shown = []
        self.tree_view.modify_font(pango.FontDescription("arial 8"))

    def create_list(self):
        """Tree view is filled with cells, window gets scrollbars.
        Returns self.scrolled_window"""
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolled_window.add_with_viewport(self.tree_view)
        self.tree_view.show()

        timecell = gtk.CellRendererText()
        msgcell = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Time", timecell, text=0)
        self.tree_view.append_column(column)
        column = gtk.TreeViewColumn("Tweet", msgcell, text=1)
        self.tree_view.append_column(column)
        return self.scrolled_window

    def stream_updated(self, data):
        """If invoked, new tweets are prepended in the view."""
        for t in data:
            if t.guid not in self.shown:
                self.shown.append(t.guid)
                self.model.prepend([t.pubDate.strftime("%m/%d %H:%M"), t.text])
