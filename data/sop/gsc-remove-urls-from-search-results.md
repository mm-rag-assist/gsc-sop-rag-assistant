---
doc_id: gsc-remove-urls-from-search-results
title: "GSC - Remove URLs from search results"
tool: Google Search Console
source: "DemoCorp Search Support SOP (anonymized)"
language: en
---

# GSC - Remove URLs from search results

This document aims to provide a **Standard Operating Procedure** for removing URLs from search results using Google Search Console.

## How to remove URLs from search results

1. If the request is not assigned yet, assign it to yourself in the TicketDesk platform by clicking the ***Assign to Me*** button.
2. Start working on the request by clicking the ***Begin Work*** button.
3. Set the **Component** as **SEO / Webmaster Tools**, then click **Save**.
4. Log in to Google Search Console <https://search.google.com/search-console/about> with searchsupport@democorp.example credentials.
5. Find domain property on the list on the left-hand side. Copy/paste it or start typing its name.
6. In menu choose **Removals**.
7. On the removals page choose **NEW REQUEST**.
8. Depending on the **Description** & **Details** on the **Case Detail** in the TicketDesk ticket take necessary actions:
   1. If you have to **remove single url** follow **step 9**,
   2. If you have to **remove entire site** follow **step 10**.
9. Steps to **remove single url** from Google search results:
   1. In the New Request form fill in **Enter URL** field with page url,
   2. choose **Remove this URL only**,
   3. click **NEXT**,
   4. Confirmation window will popup, accept your choice by clicking **SUBMIT REQUEST**,
   5. After submitting, the request will have status “**Processing request**” and later on it will change to “**Temporarily removed**”.
   6. Complete the request, follow **step 11**.
10. Steps to **remove entire site** from Google search results:
    1. In the New Request form fill in **Enter URL** field with full domain url, including https:// or http://,
    2. choose **Remove all URLs with this prefix**,
    3. click **NEXT**,
    4. Confirmation window will popup, accept your choice by clicking **SUBMIT REQUEST**,
    5. After submitting, the request will have prefix ***“Starts with:”*** and status “**Processing request**” and later on it will change to “**Temporarily removed**”,
    6. Complete the request, follow **step 11**.
11. Complete the request:
    1. Respond to the requestor in **Work Notes** in **Additional comments (Customer visible)**, for example:

       ```text
       The listed URLs have been reported to GSC for removal.

       Once this ticket is closed, you'll receive a brief survey about our support. We'd appreciate your feedback.

       Kind regards,
       ```
    2. In **Closure Information** write **URLs removal submitted**.
    3. Choose **Fulfilled** in **Closure Code**.
    4. Click **Complete work**.
    5. The next day, if there are no comments from the requestor, click **Close record**.
