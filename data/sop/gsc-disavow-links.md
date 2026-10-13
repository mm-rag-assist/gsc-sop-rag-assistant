---
doc_id: gsc-disavow-links
title: "GSC - Disavow links"
tool: Google Search Console
source: "DemoCorp Search Support SOP (anonymized)"
language: en
---

# GSC - Disavow links

This document aims to provide a **Standard Operating Procedure** for disavowing links in Google Search Console.

## How to upload Disavow links file in GSC?

1. If the request is not assigned yet, assign it to yourself in the TicketDesk platform by clicking the ***Assign to Me*** button.
2. Start working on the request by clicking the ***Begin Work*** button.
3. Set the **Component** as **SEO / Webmaster Tools**, then click **Save**.
4. Check URL property in the request - you can find it in **Website/Application** box or in the ticket **Details**.
5. Log in to Google Search Console <https://search.google.com/search-console/disavow-links> with **searchsupport2@democorp.example** credentials.
6. In GSC select URL property using drop down menu.
7. Download attached disavow file(s) from the ticket and review it carefully (check if there are any proper domains, e.g. existing DemoCorp domains or proper blog pages).
   - If the file is correct, then follow step 8.
   - If the file needs to be revised, then follow step 13.
8. If this is the first disavow for a particular domain, choose **Upload disavow list** button and upload disavow txt file.
9. If there was a disavow file previously uploaded, you must replace file with a new one using **Replace** button.
10. If the file was uploaded successfully go to step 11, else go to step 12.
11. Complete the request:
    1. Respond to the requestor in **Work Notes** in **Additional comments (Customer visible)**, for example:

       ```text
       Hello,

       I've just successfully uploaded the file in Google Search Console for brand-one.example (see the screenshot attached).

       Once this ticket is closed, you'll receive a brief survey about our support. We'd appreciate your feedback.

       Kind regards,
       ```
    2. In **Closure Information** write **Disavow file uploaded**.
    3. Choose **Fulfilled** in **Closure Code**.
    4. Click **Complete work**.
    5. The next day, if there are no comments from the requestor, click **Close record**.
12. If, while uploading the file in GSC, you receive an error, attach the screenshot of the error in the ticket and respond to the requestor.

    **Reply to requestor** (customer visible):

    ```text
    I've received the following error in GSC:

    "The file could not be uploaded or applied due to the following errors. Any previous list will not be replaced."

    Please make the necessary corrections in the disavow links file and send it back.

    This may help: https://support.google.com/webmasters/answer/2648487?hl=en
    ```
13. If the file contains working DemoCorp domains or has been created incorrectly, choose one of the reply templates below and wait for response or [reject the ticket](#how-to-reject-a-ticket) accordingly.

### Reply templates – incorrect disavow file

**Template 1 – file contains DemoCorp-owned domains, ticket rejected** (customer visible):

```text
Hello,

I have to reject this ticket because the disavow file contains DemoCorp owned domains (e.g. democorp.example.cn, brand-two.example.cn). Reporting these domains as potentially harmful with Disavow Tool in Google Search Console can negatively impact the entire DemoCorp domain ecosystem.

All disavow files prepared automatically by tools should be reviewed manually. Some indicated DemoCorp domains have been marked as potentially toxic because they do not have SSL certificates working. However, this does not mean that the links derived from this domains are harmful.

More helpful information on disavow feature in GSC:
https://support.google.com/webmasters/answer/2648487?hl=en

Please prepare a new disavow file, review/check all the domains carefully and raise a new ticket.

If you have any questions, you can contact our team at searchsupport@democorp.example
```

**Template 2 – file incorrectly prepared, requestor asked to prepare it again** (customer visible):

```text
Hello,

I have reviewed the file you sent and unfortunately it's incorrectly prepared.

It should contain really malicious or toxic domains. There is no reason to disavow redirected domains that are owned by DemoCorp (e.g. brand-three.example, brand-four.democorp.example, etc. = see the screenshots attached). They are definitely not harmful.

Google states the following: "We recommend that you only disavow backlinks if you believe that there are a considerable number of spammy, artificial, or low-quality links pointing to your site, and if you are confident that the links are causing issues for you."

More information here:
https://support.google.com/webmasters/answer/2648487?hl=en

Prepare the list again and send it to me once it's ready.

Thank you
```

**Template 3 – file uploaded after excluding DemoCorp-owned domains** (customer visible):

```text
Hello,

I have uploaded the provided disavow file in Google Search Console. However, I have excluded the following domains, that are owned by DemoCorp and redirected to brand-five.example:
- brand-five-tips.example
- brand-five-gel.example

This time I looked through the list of domains one by one, because it is short. Next time, please prepare your list more carefully. It should contain really malicious or toxic domains. There is no reason to disavow redirected domains that are owned by DemoCorp. They are definitely not harmful.

Google states the following: "We recommend that you only disavow backlinks if you believe that there are a considerable number of spammy, artificial, or low-quality links pointing to your site, and if you are confident that the links are causing issues for you."
```

## How to reject a ticket?

1. Go to **Closure Information** tab and write the reason for ticket rejection in **Resolution Notes** and choose **Request Rejected** in **Closure Code**. For example: Incorrectly prepared disavow file.
2. Click **Complete work**.
3. Then, click **Close record**.
