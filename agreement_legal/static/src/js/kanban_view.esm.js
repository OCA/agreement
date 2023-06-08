/** @odoo-module **/

import {registry} from "@web/core/registry";
import {KanbanController} from "@web/views/kanban/kanban_controller";
import {kanbanView} from "@web/views/kanban/kanban_view";
import {useService} from "@web/core/utils/hooks";

export class AgreementKanbanController extends KanbanController {
    setup() {
        super.setup();
        this.action = useService("action");
        this.canCreateTemplate = this.props.context.default_is_template || false;
    }
    onClickCreateFromTemplate() {
        this.action.doAction("agreement_legal.create_agreement_from_template_action");
    }
}

export const AgreementKanbanView = {
    ...kanbanView,
    Controller: AgreementKanbanController,
    buttonTemplate: "agreement.KanbanView.Buttons",
};

registry.category("views").add("agreement_template_kanban", AgreementKanbanView);
