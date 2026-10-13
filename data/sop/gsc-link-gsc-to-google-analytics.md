---
doc_id: gsc-link-gsc-to-google-analytics
title: "GSC - Link GSC to Google Analytics"
tool: Google Search Console
source: "DemoCorp Search Support SOP (anonymized)"
language: en
---

# GSC - Link GSC to Google Analytics

This document is intended to provide a **Standard Operating Procedure** for linking Google Search Console to Google Analytics.

## How to link Google Search Console to Google Analytics?

1. If the request is not assigned yet, assign it to yourself in the TicketDesk platform by clicking the ***Assign to Me*** button.
2. Start working on the request by clicking the ***Begin Work*** button.
3. Set the **Component** as **SEO / Webmaster Tools**, then click **Save**.
4. In **Case Detail** check the ticket’s **Details**, where the requestor should provide website name and details what to connect to.
5. Log in to Google Analytics <https://analytics.google.com> using the searchsupport@democorp.example credentials.
6. To access the GA property, select it from the drop-down menu located at the top of the page.
7. In the search bar, input the domain name and select the corresponding Google Analytics property.
8. Next, access the **Admin settings** located in the bottom left corner of the screen once the page has loaded.
9. Scroll down to the **Product links** section and select **Search Console links**.
10. Next choose **Link** button.
11. On the next screen click **Choose accounts**.
12. Click on the search bar and type in the domain name. Select the appropriate domain name from the list and tick the box. Then, click on the **Confirm** button.
13. Then click **Next**.
14. Select Web Stream – click **Select** and choose a data stream from the list by clicking **Choose**.
15. Confirm setup by clicking **Next**.
16. Verify data and if everything is properly set up click **Submit**.
17. A window confirming the action will be displayed.
18. The current status will also appear on the admin page of the Search Console links.
19. If the requestor needs a screenshot, you can send him/her such screenshot.
20. Report the indexing in *DemoCorp WMT Access/Verification Requests Management* file in ***Other*** tab.
21. Fill in (screenshots omitted in this version):
    - Status (YTS=yet to start, WIP=work in progress, CLD=completed, SUSP=suspended)
    - Search engine: Google
    - Type: Linking to GA4
    - Requested URL/Website (paste website domain name)
    - \# of requests (number of domains)
    - Close Date
    - Open Date
    - Ticket (paste the number of ticket)
    - Person Responsible (person that was assigned to manage the ticket)
22. Complete the request:
    1. Respond to the requestor in **Work Notes** in **Additional comments (Customer visible)**, for example:

       ```text
       The GSC domain property [domain name] has been successfully connected to the GA4 property.

       Once this ticket is closed, you'll receive a brief survey about our support. We'd appreciate your feedback.

       Kind regards,
       ```
    2. In **Closure Information** write **Linking to GA4 completed**.
    3. Choose **Fulfilled** in **Closure Code**.
    4. Click **Complete work**.
    5. The next day, if there are no comments from the requestor, click **Close record**.

## Troubleshooting

### How to remove account link?

If you have linked the wrong accounts, you may need to remove the link. To do this, follow steps 5-9 and continue with the additional steps below.

1. On the Search Console links page, click current connection on the list.
2. Click three dots in the right top corner.
3. Click Delete from menu.
4. If you are sure click Delete again in the popup window.

### How to link accounts when permission level is too low?

When attempting to merge Google Analytics 4 (GA4) properties with Google Search Console (GSC), users may encounter problems due to insufficient permission levels. If you do not have administrator access to GA4 properties, you will not be able to complete the connection process.

If this is a new domain then drop an email to the GA Product Owner to align and obtain admin access for new GA4 property for email <searchsupport@democorp.example>.

As an alternative method, follow the steps below:

1. Request Admin Access: create a chatroom or write an email to <web-analytics@democorp.example> to inform Web Analytics of new DemoCorp website linking request and the time window for required GA4 admin access.
2. Link accounts – follow steps 5 and above.
3. Access will be revoked post-linking.
