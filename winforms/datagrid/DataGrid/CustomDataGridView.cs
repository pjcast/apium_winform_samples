using System;
using System.Collections.Generic;
using System.Text;
using System.Windows.Forms;

namespace DataGrid
{
    public class CustomDataGridView : DataGridView
    {
        private string myCustomProp = "MyCustomProperty";

        public string MyCustomProp
        { 
            get => myCustomProp; 
            set => myCustomProp = value;
        }

        protected override AccessibleObject CreateAccessibilityInstance()
        {
            var baseInstance = base.CreateAccessibilityInstance();
            return new UserControl1AccessibleObject(this, baseInstance);
        }

        protected class UserControl1AccessibleObject : DataGridViewAccessibleObject// ControlAccessibleObject
        {
            public UserControl1AccessibleObject(CustomDataGridView ownerControl, AccessibleObject accessibleObject)
                : base(ownerControl)
            {
                AccessibleObject = accessibleObject;
                _itemCount = AccessibleObject.GetChildCount() + 1;
            }

            AccessibleObject AccessibleObject { get; }

            public new CustomDataGridView Owner
            {
                get
                {
                    return (CustomDataGridView)base.Owner;
                }
            }

            private int _itemCount = 1;

            public override int GetChildCount()
            {
                _itemCount = AccessibleObject.GetChildCount() + 1;
                return _itemCount;
                //return AccessibleObject.GetChildCount();
            }

            public override AccessibleObject GetChild(int index)
            {
                AccessibleObject result = null;
                if (index == 0)
                    result = new ValueAccessibleObject("MyCustomProp", Owner.MyCustomProp, this);
                else
                    result = AccessibleObject.GetChild(index - 1);

                return result;
            }
        }
    }

    public class ValueAccessibleObject : AccessibleObject
    {
        private string _name;
        private string _value;

        public ValueAccessibleObject(string name, string value, AccessibleObject parent)
        {
            _name = name;
            _value = value;
            Parent = parent;
        }

        public override AccessibleObject Parent { get; }

        public override AccessibleRole Role
        {
            get
            {
                //return AccessibleRole.Text; // activate Value pattern
                return AccessibleRole.Text;
            }
        }

        // note you need to override with member values, base value cannot always store something
        public override string Value { get { return _value; } set { _value = value; } }
        public override string Name { get { return _name; } }
    }
}
