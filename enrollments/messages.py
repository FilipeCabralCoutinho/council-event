from .models import Parcela

def text_fallback_new(enrollment):
    return f"""
        Confirmação de inscrição – IX Concílio da 6ª Região


        Graça e paz!

        Recebemos com alegria a sua inscrição no IX Concílio Regional.
        Será um tempo especial de comunhão, crescimento e direcionamento
        de Deus para todos nós. Para concluir o seu processo de participação,
        pedimos que envie os comprovantes de pagamento EXCLUSIVAMENTE para este
        mesmo e-mail. Sem o envio dos comprovantes, a Inscrição será CANCELADA.
        Assim que o pagamento for confirmado no total, você receberá o seu
        voucher de acesso ao Acampamento Efraim, que garantirá sua entrada
        no evento.
        
        Ficamos felizes por ter você conosco nesse momento tão importante!
        
        Qualquer dúvida, estamos à disposição.
        
        Deus abençoe!

        Atenciosamente,
        Organização do IX Concílio Regional

        ==============================
        DADOS DA INSCRIÇÃO
        ==============================

        NR INSCR: {enrollment.id}
        NOME: {enrollment.nome}
        DISTRITO: {enrollment.distrito}
        IGREJA: {enrollment.igreja}
        CELULAR: {enrollment.whatsapp}
        FUNÇÃO: {enrollment.funcao}
        APTO CONCÍLIO GERAL?: {enrollment.apto_concilio}
        POSSUI COMORBIDADE?: {enrollment.possui_comorbidade}
        QUAL COMORBIDADE?: {enrollment.qual_comorbidade}
        PERNOITE?: {enrollment.pernoite}
        STATUS PAGAMENTO: {enrollment.status_pagamento}

        ==============================
        INFORMAÇÕES DO EVENTO
        ==============================

        Data:
        26, 27 e 28 de novembro de 2026

        Local:
        Acampamento Efraim

        ==============================
        DÚVIDAS
        ==============================

        Em caso de dúvidas, entre em contato com a organização.

        Igreja Metodista Wesleyana
        6ª Região
        """

def start_text_new():
    return (
            """
            Graça e paz            Recebemos com alegria a sua inscrição no IX Concílio Regional. Será um tempo especial de comunhão, crescimento e direcionamento de Deus para todos nós.<br><br>
            <strong>Para concluir o seu processo de participação, pedimos que envie os comprovantes de pagamento exclusivamente para este mesmo e-mail. Sem o envio dos comprovantes a Inscrição será cancelada.</strong><br><br>
            Assim que o pagamento for confirmado no total, você receberá o seu voucher de acesso ao Acampamento Efraim, que garantirá sua entrada no evento.

            Ficamos felizes por ter você conosco nesse momento tão importante!

            Qualquer dúvida, estamos à disposição.

            Deus abençoe!

            Atenciosamente,
            Organização do IX Concílio Regional
            """
        )


def text_fallback_payment_confirmation(enrollment):
    return f"""
        Pagamento confirmado – IX Concílio da 6ª Região


        Graça e paz!

        Seu pagamento foi confirmado com sucesso! Agradecemos muito por
        concluir este importante passo para sua participação no IX Concílio Regional.

        Em breve, você receberá seu voucher de acesso ao Acampamento Efraim,
        que garantirá sua entrada no evento. Mantenha este e-mail em local seguro
        para referência futura.

        Ficamos felizes por ter você conosco nesse momento tão importante!

        Qualquer dúvida, estamos à disposição.

        Deus abençoe!

        Atenciosamente,
        Organização do IX Concílio Regional

        ==============================
        DADOS DA INSCRIÇÃO
        ==============================

        NR INSCR: {enrollment.id}
        NOME: {enrollment.nome}
        DISTRITO: {enrollment.distrito}
        IGREJA: {enrollment.igreja}
        STATUS PAGAMENTO: {enrollment.status_pagamento}

        ==============================
        INFORMAÇÕES DO EVENTO
        ==============================

        Data:
        26, 27 e 28 de novembro de 2026

        Local:
        Acampamento Efraim

        ==============================
        DÚVIDAS
        ==============================

        Em caso de dúvidas, entre em contato com a organização.

        Igreja Metodista Wesleyana
        6ª Região
        """


def start_text_payment_confirmation():
    return (
            """
            Graça e paz!

            Seu pagamento foi confirmado com sucesso! Agradecemos muito por concluir este importante passo para sua participação no IX Concílio Regional.

            Em breve, você receberá seu voucher de acesso ao Acampamento Efraim, que garantirá sua entrada no evento.

            Ficamos felizes por ter você conosco nesse momento tão importante!

            Qualquer dúvida, estamos à disposição.

            Deus abençoe!

            Atenciosamente,
            Organização do IX Concílio Regional
            """
        )

def text_fallback_update_payment(enrollment):
    enrollment_id = enrollment.id
    pagamento = enrollment.pagamento
    parcelas = Parcela.objects.filter(pagamento=pagamento)
    text_parcelas = ""

    for parcela in parcelas:
        text_parcelas += f"Parcela {parcela.numero}: R$ {parcela.valor:.2f} - Status: {parcela.status}\n"

    return f"""
        Atualização de pagamento – IX Concílio da 6ª Região

        Graça e paz!

        Houve uma atualização no seu pagamento. As informações atuais são:

        NR INSCR: {enrollment.id}
        NOME: {enrollment.nome}
        Parcelas: {enrollment.quantidade_parcelas}
        {text_parcelas}

        ==============================
        INFORMAÇÕES DO EVENTO
        ==============================

        Data:
        26, 27 e 28 de novembro de 2026

        Local:
        Acampamento Efraim

        ==============================
        DÚVIDAS
        ==============================

        Em caso de dúvidas, entre em contato com a organização do evento pelo grupo do whatsapp.

        Igreja Metodista Wesleyana
        6ª Região
        """

def start_text_update_payment():
    return """
            Atualização de pagamento – IX Concílio da 6ª Região

            Graça e paz!
            
            Houve uma atualização no seu pagamento. As informações atuais são:
        """