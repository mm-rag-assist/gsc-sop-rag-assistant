---
doc_id: gsc-request-indexing
title: "GSC - Request indexing"
tool: Google Search Console
source: "DemoCorp Search Support SOP (anonymized)"
language: en
---

# GSC - Request indexing

This document aims to provide a **Standard Operating Procedure** for indexing requests in Google Search Console.

## Important – daily indexing limit

Please note that you can request indexing in GSC for about 9-11 URLs per day. After exactly 24h you’ll be able to request indexing for the new batch of URLs. If the requestor sends you more than 11 URLs, you may need to work on the ticket for more than 1-2 days.

You have to monitor the URLs you requested indexing for and keep in mind the URLs which are still waiting. Remember to work on the ticket day by day requesting 9-11 URLs every single day.

**Example:** If someone sends 38 URLs for indexing, you will probably have to request indexing for 10 URLs/1st day – 10 URLs/2nd day – 10 URLs/3rd day – 8 URLs/4th day.

## How to request indexing?

1. If the request is not assigned yet, assign it to yourself in the TicketDesk platform by clicking the ***Assign to Me*** button.
2. Start working on the request by clicking the ***Begin Work*** button.
3. Set the **Component** as **SEO / Webmaster Tools**, then click **Save**.
4. In **Case Detail** check the ticket’s **Details**, where the requestor should provide short description and urls to index:
   1. you can find URLs directly in details,
   2. or you can find URLs in attachment and you need to download and open the file.
5. Log in to Google Search Console <https://search.google.com/search-console/about> with searchsupport@democorp.example credentials.
6. Find domain property on the list on the left-hand side. Copy/paste it or start typing its name.
7. In the inspect field paste given url to index and click “Enter” key.
8. Click **REQUEST INDEXING**.
9. You should see popup window.
10. If the indexing is successful, you will receive information “Indexing requested”, click **GOT IT**.
11. If the requestor needs a screenshot, you can send him/her such screenshot.
12. Repeat steps 7-11 until you have requested indexing of all specified URLs, respecting the daily requests limit.
13. Report the indexing in *DemoCorp WMT Access/Verification Requests Management* file in **Other** tab.
14. Fill in (screenshots omitted in this version):
    - Status (YTS=yet to start, WIP=work in progress, CLD=completed, SUSP=suspended)
    - Search engine: Google
    - Type: Re-indexing
    - Requested URL/Website (paste the URLs you requested indexing for)
    - \# of requests (number of URLs)
    - Close Date
    - Open Date
    - Ticket (paste the number of ticket)
    - Person Responsible (person that was assigned to manage the ticket)
15. Complete the request:
    1. Respond to the requestor in **Work Notes** in **Additional comments (Customer visible)**. Use one of the reply templates below.
    2. In **Closure Information** write **Indexing requested**.
    3. Choose **Fulfilled** in **Closure Code**.
    4. Click **Complete work**.
    5. The next day, if there are no comments from the requestor, click **Close record**.

### Reply templates – indexing requested

**Template 1 – several URLs** (customer visible):

```text
Hello,
I have just requested indexing for the following URLs:

[URL]
[URL]
[URL]

Once this ticket is closed, you'll receive a brief survey about our support. We'd appreciate your feedback.

Kind regards,
```

**Template 2 – one URL** (customer visible):

```text
Hello,
Indexing has just been requested for: [URL].

Once this ticket is closed, you'll receive a brief survey about our support. We'd appreciate your feedback.

Kind regards,
```

**Template 3 – one URL, alternative wording** (customer visible):

```text
Hello,
I've just requested indexing for [URL] in Google Search Console.

Once this ticket is closed, you'll receive a brief survey about our support. We'd appreciate your feedback.

Kind regards,
```

## What if the requestor didn’t send any URLs for indexing?

1. Respond to the requestor in **Work Notes** in **Additional comments (Customer visible)**:

   ```text
   Send us the URLs you need to request indexing in GSC for, please.
   ```
2. Wait 1-2 business days for the requestor’s response.
