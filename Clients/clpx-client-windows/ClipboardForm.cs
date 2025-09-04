using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace clpx_client_windows {
    public partial class ClipboardForm : Form {
        public ClipboardForm() {
            InitializeComponent();
            this.Text = "clpx clipboard";
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
        }

        private void ClipboardForm_Load(object sender, EventArgs e) {}
    }
}
