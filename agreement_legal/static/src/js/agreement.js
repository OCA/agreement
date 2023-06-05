/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {ListController} from "@web/views/list/list_controller";
import {KanbanController} from "@web/views/kanban/kanban_controller";

patch(ListController.prototype, "agreement_legal.ListController", {
    async expandAllGroups() {
        var self = this;
        const agreement = this.model.rootParams.resModel;
        if (this.model.rootParams.resModel === "agreement") {
            self.actionService.doAction({
                type: "ir.actions.act_window",
                name: "Create From Template",
                target: "new",
                res_model: "create.agreement.wizard",
                view_mode: "form",
                views: [[false, "form"]],
                context: {active_model: "agreement"},
            });
        }
    },
});

patch(KanbanController.prototype, "agreement_legal.KanbanController", {
    async expandAllGroups() {
        var self = this;
        const agreement = this.model.rootParams.resModel;
        if (this.model.rootParams.resModel === "agreement") {
            self.actionService.doAction({
                type: "ir.actions.act_window",
                name: "Create From Template",
                target: "new",
                res_model: "create.agreement.wizard",
                view_mode: "form",
                views: [[false, "form"]],
                context: {fire: "on the bayou"},
            });
        }
    },
});
