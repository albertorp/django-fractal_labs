from simple_mail.mailer import BaseSimpleMail, simple_mailer


class RequirementAcknowledgeMail(BaseSimpleMail):
    email_key = 'requirement_acknowledge'

simple_mailer.register(RequirementAcknowledgeMail)


class RequirementReturnMail(BaseSimpleMail):
    email_key = 'requirement_return'

    def set_context(self, comment):
        self.context = {
            'comment': comment
        }

simple_mailer.register(RequirementReturnMail)


class RequirementRejectMail(BaseSimpleMail):
    email_key = 'requirement_reject'

    def set_context(self, comment):
        self.context = {
            'comment': comment
        }

simple_mailer.register(RequirementRejectMail)




class QuotationSendMail(BaseSimpleMail):
    email_key = 'quotation_send'

    def set_context(self, comment):
        self.context = {
            'comment': comment
        }

simple_mailer.register(QuotationSendMail)


class JobAssignMail(BaseSimpleMail):
    email_key = 'job_assign'

    def set_context(self, comment):
        self.context = {
            'comment': comment
        }

simple_mailer.register(JobAssignMail)


class JobToReviewMail(BaseSimpleMail):
    email_key = 'job_to_review'

    def set_context(self, comment):
        self.context = {
            'comment': comment
        }

simple_mailer.register(JobToReviewMail)


class JobForCorrectionMail(BaseSimpleMail):
    email_key = 'job_for_correction'

    def set_context(self, comment):
        self.context = {
            'comment': comment
        }

simple_mailer.register(JobForCorrectionMail)


class JobDeliverMail(BaseSimpleMail):
    email_key = 'job_deliver'

    def set_context(self, comment):
        self.context = {
            'comment': comment
        }

simple_mailer.register(JobDeliverMail)


class JobForReworkMail(BaseSimpleMail):
    email_key = 'job_for_rework'

    def set_context(self, comment):
        self.context = {
            'comment': comment
        }

simple_mailer.register(JobForReworkMail)


