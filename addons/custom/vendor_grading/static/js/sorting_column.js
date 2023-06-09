odoo.define('sg_vendor_grading.sorting_column', function (require){
    'use strict'

    $(document).ready(function() {
        var element = $("div.o_list_view.o_purchase_order .table-responsive .o_list_table thead tr th:nth-child(6)")
        if (element){
            element.addClass("o_column_sortable");
        }
    })

//    setTimeout(function(){
//        var element = $("div.o_list_view.o_purchase_order .table-responsive .o_list_table thead tr th:nth-child(6)")
//        if(element) {
//            element.addClass("sort o_column_sortable");
//        }
//    },)
});