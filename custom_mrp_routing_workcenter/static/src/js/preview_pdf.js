/** @odoo-module alias=custom_mrp_routing_workcenter.PreviewAttachment **/
"use strict";
import relational_fields from 'web.relational_fields';
var ajax = require('web.ajax');
var rpc = require('web.rpc');
var Viewer = require('ks_curved_backend_theme.KsListDocumentViewer');


var FieldMany2ManyBinaryMultiFiles = relational_fields.FieldMany2ManyBinaryMultiFiles;

var FieldMany2ManyBinaryMultiFilesPreview = FieldMany2ManyBinaryMultiFiles.include({
    events: _.extend({
        'click .attachment_preview': '_on_PreviewAttachment',
        'click .ks_binary_file_preview': "ks_onAttachmentView",
    }, FieldMany2ManyBinaryMultiFiles.prototype.events),

    _on_PreviewAttachment: function (ev) {
        var self = this;
        console.log(ev.currentTarget)
        var fileID = $(ev.currentTarget).data('id');
        var title = $(ev.currentTarget).data('title');
        var url='/web/content/' + fileID
        var wnd=window.open(url, '_blank', 'fullscreen=yes','location=no')
        setTimeout(function(){ wnd.document.title = title; }, 1000);
    },
    ks_onAttachmentView: function(ev) {
            var self = this;
            try {
                ev.preventDefault();
                ev.stopPropagation();
                var ks_mimetype = self.recordData.mimetype;
                function ks_docView(ks_file_data) {
                    if (ks_file_data) {
                        var match = ks_file_data.type.match("(image|video|application/pdf|text)");
                        if(match){
                            var ks_attachment = [{
                                filename: ks_file_data.name,
                                id: ks_file_data.id,
                                is_main: false,
                                mimetype: ks_file_data.type,
                                name: ks_file_data.name,
                                type: ks_file_data.type,
                                url: "/web/content/" + ks_file_data.id + "?download=true",
                            }]
                            var ks_activeAttachmentID = ks_file_data.id;
                            var ks_attachmentViewer = new Viewer(self,ks_attachment,ks_activeAttachmentID);
                            ks_attachmentViewer.appendTo($('body'));
                        }
                        else{
                            alert('This file type can not be previewed.')
                        }
                    }
                }
                if (ks_mimetype) {
                    ks_file_data = {
                        'id': self.recordData.id,
                        'type': self.recordData.mimetype || 'application/octet-stream',
                        'name': self.recordData.name || self.recordData.display_name || "",
                    }
                    ks_docView(ks_file_data);
                } else {
                    var fileID = $(ev.currentTarget).data('id');
                    console.log(fileID);
                    rpc.query({
                      model: 'mrp.routing.workcenter',
                      method: 'get_attachment',
                      args: [fileID]
                    }).then(function(result) {
                        var def = ajax.jsonRpc("/get/record/details", 'call', {
                            'res_id': result['res_id'],
                            'model': result['res_model'],
                            'res_field': result['res_field'],
                        });
                        return $.when(def).then(function(vals) {
                            if (vals && vals.id) {
                                ks_docView(vals);
                            } else {
                                alert('The preview of the file can not be generated as it does not exist in the Odoo file system (Attachments).')
                            }
                        });
                    });
                }
            } catch (err) {
                alert(err);
            }
        },
});
export default FieldMany2ManyBinaryMultiFilesPreview
