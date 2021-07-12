from jira import JIRA


def authentication(host, username, token):
    """"Authentication to Jira.
    Args:
        host: hostname of jira instance
        username: username to access jira
        token: password or token. Users who use social authentications can create a token form their front-ends
    """
    try:
        options = {'server': host}
        jira = JIRA(options, basic_auth=(username, token))
        return jira
    except Exception as e:
        return e


def ticket_search(service, query, maxresults=None):
    """"Search tickets
    Args:
        service: jira service created from authentication() function
        query: JQL to filter out tickets
        maxresults: maximum of number or outputs
    """
    try:
        tickets = service.search_issues(query, maxResults=maxresults)
        return tickets
    except Exception as e:
        return e


def get_ticket_attribute(service, ticket, attribute):
    """Obtain different ticket attributes

    Args:
        service: jira service created from authentication() function
        ticket: specific ticket number eg: PROD-1111
        attribute: diffrent elements in ticket eg: title, creator etc...

    Supported attributes: summary, description, assignee, created, status, priority, reporter, creator,
    issuelinks, watches, resolver, validator, fixedbinaryversion, targetststem, approver, fixVersions, comment
    """
    try:
        ticket = service.issue(ticket)
    except Exception as e:
        return e

    attribute_dict = {
        "title": ticket.fields.summary,
        "description": ticket.fields.description,
        "status": ticket.fields.status,
        "environment": ticket.fields.environment,
        "assignee": ticket.fields.assignee,
        "reporter": ticket.fields.reporter,
        "targetststem": ticket.fields.customfield_10201,
        "fixedbinaryversion": ticket.fields.customfield_10300,
        "approver": ticket.fields.customfield_11420,
        "validator": ticket.fields.customfield_11439,
        "resolver": ticket.fields.customfield_11442,
        "fixVersions": ticket.fields.fixVersions,
        "created": ticket.fields.created,
        "priority": ticket.fields.priority,
        "issuelinks": ticket.fields.issuelinks,
        "watches": ticket.fields.watches,
        "comment": ticket.fields.comment.comments,

    }

    if attribute in attribute_dict:
        try:
            return attribute_dict.get(attribute)
        except Exception as e:
            return e
    else:
        return "Field Name still not supported"


def create_ticket(service, project, summary, description, issuetype, assignee, attachments=[]):
    """"Create a jira ticket
    Args:
        service: jira service created from authentication() function
        project: the project the ticket needed to be created. eg: PROD, REQ, NATMOBILE
        summary: title of the ticket
        description: description or the ticket
        issuetype: type of the issue eg: Task, Bug
        assignee: the person the ticket should assigned eg: vidura.d
        attachments: images or other files needed to attached to the ticket. Should be a list
    """
    try:
        new_issue = service.create_issue(project=project,  summary=summary, issuetype={'name': issuetype},
                                         description=description, assignee={'name': assignee})
    except Exception as e:
        return e
    for i in attachments:
        service.add_attachment(issue=new_issue, attachment=i)


def update_ticket(service, ticket, field, value):
    """"Change specific attribute of a ticket

    Args:
        service: jira service created from authentication() function
        ticket: specific ticket number eg: PROD-1111
        field: the attribute needed to change
        value: new value of the attribute

    fields supported: summary, description, assignee, status, priority, environment
    """
    ticket = service.issue(ticket)
    if field == "assignee":
        try:
            ticket.update(assignee={'name': value})
        except Exception as e:
            return e
    elif field == "issuetype":
        try:
            ticket.update(issuetype={'name': value})
        except Exception as e:
            return e
    else:
        try:
            ticket.update(fields={field: value})
        except Exception as e:
            return e


def delete_ticket(service, ticket):
    """Change specific attribute of a ticket. You must have the sufficient permission to delete a ticket

    Args:
        service: jira service created from authentication() function
        ticket: specific ticket number eg: PROD-1111

    """
    ticket = service.issue(ticket)
    try:
        ticket.delete()
    except Exception as e:
        return e
