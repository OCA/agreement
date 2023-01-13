/** @odoo-module **/

import {registry} from "@web/core/registry";
import {FormController} from "@web/views/form/form_controller";
import {formView} from "@web/views/form/form_view";
import {useService} from "@web/core/utils/hooks";

export class AgreementFormController extends FormController {
    setup() {
        super.setup();
        this.action = useService("action");
        this.canCreateTemplate = this.props.context.default_is_template || false;
    }
    onClickCreateFromTemplate() {
        this.action.doAction("agreement_legal.create_agreement_from_template_action");
    }
}

export const AgreementFormView = {
    ...formView,
    Controller: AgreementFormController,
};

registry.category("views").add("agreement_template_form", AgreementFormView);
