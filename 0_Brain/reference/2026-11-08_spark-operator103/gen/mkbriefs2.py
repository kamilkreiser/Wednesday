src=open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_spark-operator103/gen/mkbriefs.py',encoding='utf-8').read()
exec(src.split('# ---- P1')[0])
tp4=SV+'originate/src/__tests__/ks1937-email-service-logs-never-carry-the-recipient-address.test.ts'
t=rd('ks1937email.test.ts.tip')
last="  });\n});\n"
assert t.endswith(last)
cells='''  });

  it('E8 the allow-list refusal line carries no part of the recipient address either: not even its domain', async () => {
    const email = loadEmail({ ...SMTP_ENV, EMAIL_RECIPIENT_ALLOWLIST: 'someone.else@example.test' });
    await expect(email.sendEmail({ to: 'ks2099.person@ks2099-domain.invalid', subject: 'ks2099 subject', text: 'ks2099 body' })).resolves.toBe(false);
    expect(lines('refusing to send')).toHaveLength(1);
    expect(mockLogged.filter((l) => l.toLowerCase().includes('ks2099-domain'))).toEqual([]);
  });

  it('E9 ACS accepts the send: the address still reaches the ACS call as the one recipient (only the LOG changed)', async () => {
    mockBeginSend.mockResolvedValue({ pollUntilDone: async () => ({ status: 'Succeeded', id: 'acs-msg-2099' }) });
    await expect(send(loadEmail(ACS_ENV))).resolves.toBe(true);
    expect(mockBeginSend).toHaveBeenCalledTimes(1);
    expect(mockBeginSend.mock.calls[0][0].recipients).toEqual({ to: [{ address: ADDRESS }] });
  });
});
'''
n=t[:-len(last)]+cells
g=dd(t,n,tp4)
e=rd('email.ts.tip')
e2=once(e,"console.warn(`[Email] Recipient not in EMAIL_RECIPIENT_ALLOWLIST — refusing to send`);","console.warn(`[Email] Recipient not in EMAIL_RECIPIENT_ALLOWLIST — refusing to send: ${options.to.split('@')[1]}`);")
e2=once(e2,"recipients: { to: [{ address: options.to }] },","recipients: { to: [{ address: '' }] },")
r=dd(e,e2,SV+'originate/src/services/email.ts')
brief('ks_2099_o103_p4_email_log_domain_and_acs_recipient',2099,'KS-2099 item 3: the KS-1937 email-service cells stay green when the refusal line logs the recipient domain, and the ACS recipient is unpinned (TEST-ONLY: two cells E8, E9)','KS-2099 item 3 (QA gate 235, finding F5, MINOR, MEASURED AT RUNTIME: tamper X leaves all 12 cells green; the ACS path\'s "the address still reaches the mailer" is unpinned, only SMTP cell E6 pins it).',
 'In `services/email.ts` the allow-list refusal logs a constant line (no address). The file\'s cells look only for the FULL address, so a refusal line changed to print the recipient\'s domain stays green (tamper X). Separately, the ACS send passes `recipients: { to: [{ address: options.to }] }` to `beginSend`, and cells E1 to E3 never read beginSend\'s arguments, so blanking the ACS recipient stays green (only the SMTP cell E6 pins its `to`).',
 SV+'originate/src/services/email.ts',[tp4],
 'The two cells are in the diff above; copy them verbatim. They reuse `loadEmail`, `send`, `lines`, `mockLogged`, `mockBeginSend`, `SMTP_ENV`, `ACS_ENV` and `ADDRESS` from the file. Note the closing `});` of the existing describe is shown removed and added again because the cells go before it; a strict apply takes it.',
 'The plant is `golden_red.diff` in the brief dir (applied only in the checker\'s clone): two one-line mutations of `email.ts`, the refusal line printing `options.to.split(\'@\')[1]` (tamper X) and the ACS recipient address blanked (the ACS twin of tamper W). Each red cell fails under the plant by its own assertion.',
 '- `E8 the allow-list refusal line carries no part of the recipient address`\n- `E9 ACS accepts the send: the address still reaches the ACS call`',
 'Items 1 and 2 of KS-2099 (the SMTP failed-send line echoing the address; the third-party verifier INFO line) are product changes and are not touched here. The ACS refusal/other lines are not pinned for the domain either; only the allow-list refusal line is.',
 'shared_pkg_dir=packages/shared\nshared_pkg_name=@secuura/shared\n',g,r)
print('ok4')
