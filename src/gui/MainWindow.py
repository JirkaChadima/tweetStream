import pygtk
pygtk.require('2.0')
import gtk

from TweetPane import TweetPane

__author__="Jiri Chadima"
__date__ = "$Mar 7, 2011 10:57:34 AM$"

class MainWindow :
    """Main application window"""
    def __init__(self, client):
        """Window setup, TweetPane is created, window is shown."""
        self.client = client
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(client.username)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.resize(400, 200)

        self.pane = TweetPane()
        self.client.storage.add_listener(self.pane)

        vpaned = gtk.VPaned()
   	self.window.add(vpaned)
   	vpaned.show()
   	list = self.pane.create_list()
   	vpaned.add1(list)
   	list.show()

        self.window.show()

    def main(self):
        """GTK's threads are init + main loop is started. Client's thread is
        started."""
        gtk.gdk.threads_init()
        self.client.start()
        gtk.main()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        self.exit()

    def exit(self):
        """Closes client"""
        gtk.main_quit()
        self.client.stop()
