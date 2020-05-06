using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DataGrid
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();

            var bindingSource = new BindingSource();
            bindingSource.DataSource = new SortableBindingList<DataItem>(PopulateItems());

            var dg = new DataGridView();
            dg.Name = "dataGrid";
            dg.Dock = DockStyle.Fill;
            dg.DataSource = bindingSource;
            this.Controls.Add(dg);

            var textBox = new TextBox();
            textBox.Name = "textbox";
            textBox.Dock = DockStyle.Top;
            this.Controls.Add(textBox);
        }

        private List<DataItem> PopulateItems()
        {
            var rand = new Random();
            //var numberOfItems = rand.Next(5, 500);
            var numberOfItems = 50;
            var items = new List<DataItem>();

            for(int i = 0; i < numberOfItems; ++i)
            {
                var isOddRow = i % 2 == 0;
                items.Add(new DataItem { Name = $"item{i}", Description = isOddRow ? "" : "--", Checked = isOddRow });
            }

            return items;
        }
    }

    public class DataItem
    {
        public string Name { get; set; }
        public string Description { get; set; }
        public bool Checked  { get; set; }
    }

    public class SortableBindingList<T> : BindingList<T>
    {
        private bool isSortedValue;
        ListSortDirection sortDirectionValue;
        PropertyDescriptor sortPropertyValue;

        public SortableBindingList()
        {
        }

        public SortableBindingList(IList<T> list)
        {
            foreach (object o in list)
            {
                this.Add((T)o);
            }
        }

        protected override void ApplySortCore(PropertyDescriptor prop,
            ListSortDirection direction)
        {
            Type interfaceType = prop.PropertyType.GetInterface("IComparable");

            if (interfaceType == null && prop.PropertyType.IsValueType)
            {
                Type underlyingType = Nullable.GetUnderlyingType(prop.PropertyType);

                if (underlyingType != null)
                {
                    interfaceType = underlyingType.GetInterface("IComparable");
                }
            }

            if (interfaceType != null)
            {
                sortPropertyValue = prop;
                sortDirectionValue = direction;

                IEnumerable<T> query = base.Items;

                if (direction == ListSortDirection.Ascending)
                {
                    query = query.OrderBy(i => prop.GetValue(i));
                }
                else
                {
                    query = query.OrderByDescending(i => prop.GetValue(i));
                }

                int newIndex = 0;
                foreach (object item in query)
                {
                    this.Items[newIndex] = (T)item;
                    newIndex++;
                }

                isSortedValue = true;
                this.OnListChanged(new ListChangedEventArgs(ListChangedType.Reset, -1));
            }
            else
            {
                throw new NotSupportedException("Cannot sort by " + prop.Name +
                    ". This" + prop.PropertyType.ToString() +
                    " does not implement IComparable");
            }
        }

        protected override PropertyDescriptor SortPropertyCore
        {
            get { return sortPropertyValue; }
        }

        protected override ListSortDirection SortDirectionCore
        {
            get { return sortDirectionValue; }
        }

        protected override bool SupportsSortingCore
        {
            get { return true; }
        }

        protected override bool IsSortedCore
        {
            get { return isSortedValue; }
        }
    }
}
