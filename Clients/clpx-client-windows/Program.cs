namespace clpx_client_windows {
    internal static class Program {
        private static NotifyIcon trayIcon;
        private static ContextMenuStrip trayMenu;

        [STAThread]
        static void Main() {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);


            trayMenu = new ContextMenuStrip();
            trayMenu.Items.Add("Open config", null, OnOpenConfig);
            trayMenu.Items.Add("Exit", null, OnExit);

            trayIcon = new NotifyIcon {
                Icon = System.Drawing.SystemIcons.Application,
                ContextMenuStrip = trayMenu,
                Text = "clpx-client-windows",
                Visible = true
            };

            Application.Run();
        }

        private static void OnOpenConfig(object sender, EventArgs e) {
            Form1 configForm = new Form1();
            configForm.Show();
        }

        private static void OnExit(object sender, EventArgs e) {
            trayIcon.Visible = false;
            Application.Exit();
        }
    }
}