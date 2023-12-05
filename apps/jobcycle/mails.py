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