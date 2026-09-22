# The file drawer — how it works (2026-09-22)

You asked for two things on the live board today: a Download button beside *auto-play replies* and *stop* (15:26), and the
file upload feature the local board had (15:31). Both are live at https://wednesday-dashboard-e42e.azurewebsites.net.

**Download.** The `⬇ files` button in the header opens the drawer: every file a seat has shared with you, and every file you
attached yourself. Each row shows the name, size, who placed it and when, and a one-line note. *Download* fetches the encrypted
bytes, decrypts them in your browser with your key (the same key that reads the chat), checks the sha256, then saves the file.
Without the key the rows show as locked, exactly like messages.

**Upload.** Drop a file on the conversation, or click the 📎 button next to *send*. It queues as a chip; when you send, the file
is encrypted in your browser (to your key ring and the seat's key) and the message carries the attachment. The seat reads it
with `kam_msgs.sh --fetch-attachments <dir>`. Your uploads appear in the drawer too, so you can get them back from any device.

**Bounds and posture.** 32 MiB per file. Encrypted at rest (the server only ever holds ciphertext). Every share, upload and
download is audited. Nothing is ever deleted — there is no delete route.

This README is the first file placed in the drawer, as the receipt for the build.
