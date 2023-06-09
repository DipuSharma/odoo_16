// For Open Sku Calculator Tab
odoo.define('sg_sku_calculator.calculator', function (require){
    var Widget = require('web.Widget');
    var FieldManagerMixin = require('web.FieldManagerMixin');
    var Registry = require('web.widget_registry');
    var OpenSkuCalculator = Widget.extend({
        init: function (parent, model, context)
        {
            this._super(parent);
            this._super.apply(this, arguments);
        },
        start: function() {
            var self = this;
            this._super.apply(this, arguments);
            var html ='<button id="open_sku_calculator" type="submit" class="btn btn-primary">Sku</button>';
            this.$el.html(html);
            this.$('#open_sku_calculator').click(function(ev){
                ev.preventDefault();
                ev.stopPropagation();
                $('.nav-tabs .sku_calculator a').click();
            });
            setTimeout(function(){
            var element = ""
            element = $("div.o_form_readonly .o_notebook_headers .nav-tabs .sku_calculator a");

            var element1 = $('div.o_form_readonly  #open_sku_calculator')

            if(element) {
//              element.text("Sku Generator").hide();
              element1.hide();
            } else{
//                element.text("Sku Generator").show();
                element1.show();
            }
            }, 100)
        },
    });
    require('web.widget_registry').add('open_sku_calculator_tab', OpenSkuCalculator);
    return OpenSkuCalculator;
});



//
//odoo.define('sg_sku_calculator.new_web', async function(require) {
//    'use strict';
//    let __exports = {};
//    const {registry} = require("@web/core/registry");
//    const {standardWidgetProps} = require("@web/views/widgets/standard_widget_props");
//    const {Component} = require("@odoo/owl");
//    class RibbonWidget extends Component {
//        get classes() {
//            let classes = this.props.bgClass;
//            if (this.props.text.length > 15) {
//                classes += " o_small";
//            } else if (this.props.text.length > 10) {
//                classes += " o_medium";
//            }
//            return classes;
//        }
//    }
//    RibbonWidget.template = "web.Ribbon";
//    RibbonWidget.props = {
//        ...standardWidgetProps,
//        text: {
//            type: String
//        },
//        title: {
//            type: String,
//            optional: true
//        },
//        bgClass: {
//            type: String,
//            optional: true
//        },
//    };
//    RibbonWidget.defaultProps = {
//        title: "",
//        bgClass: "bg-success",
//    };
//    RibbonWidget.extractProps = ({attrs})=>{
//        return {
//            text: attrs.title || attrs.text,
//            title: attrs.tooltip,
//            bgClass: attrs.bg_color,
//        };
//    }
//    ;
//    registry.category("view_widgets").add("dipu_ribbon", RibbonWidget);
//    return __exports;
//});
//

