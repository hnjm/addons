/** @odoo-module alias=custom_mrp_routing_workcenter.PreviewAttachment **/
"use strict";
import relational_fields from 'web.relational_fields';
var FieldMany2ManyBinaryMultiFiles = relational_fields.FieldMany2ManyBinaryMultiFiles;

var FieldMany2ManyBinaryMultiFilesPreview = FieldMany2ManyBinaryMultiFiles.include({
    events: _.extend({
        'click .attachment_preview': '_on_PreviewAttachment',
    }, FieldMany2ManyBinaryMultiFiles.prototype.events),
    _on_PreviewAttachment: function (ev) {
        var self = this;
        var fileID = $(ev.currentTarget).data('id');
        var title = $(ev.currentTarget).data('title');
        var url='/web/content/' + fileID
        var wnd=window.open(url, '_blank', 'fullscreen=yes','location=no')
        setTimeout(function(){ wnd.document.title = title; }, 1000);
    },
});
export default FieldMany2ManyBinaryMultiFilesPreview
