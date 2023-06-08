/** @odoo-module **/

import {registry} from "@web/core/registry";
import {ListController} from "@web/views/list/list_controller";
import {listView} from "@web/views/list/list_view";
import {useService} from "@web/core/utils/hooks";

export class AgreementListController extends ListController {
    setup() {
        super.setup();
        this.action = useService("action");
        this.canCreateTemplate = this.props.context.default_is_template || false;
    }
    onClickCreateFromTemplate() {
        this.action.doAction("agreement_legal.create_agreement_from_template_action");
    }
}

export const AgreementListView = {
    ...listView,
    Controller: AgreementListController,
    buttonTemplate: "agreement.ListView.Buttons",
};

registry.category("views").add("agreement_template_tree", AgreementListView);
