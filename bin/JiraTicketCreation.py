import ustocktjira

#create JIRA Ticket
def createJiraTicket(host,username,token,project,summary,description,issue,assign,attachments=[]):
    authenticate = ustocktjira.authentication(host,username,token)

    ustocktjira.create_ticket(authenticate,project,summary,description,issue,assign,attachments)
    #jqlval = 'summary ~ '+summary
    #sleep(3)
    #ticketID = ustocktjira.ticket_search(authenticate,jqlval,maxresults=None)
    #print(ticketID)

# Method to update the ticket with a comment
def updateTicketIfAvailable(host,username,token,project,summary,description):
    authenticate = ustocktjira.authentication(host, username, token)

    jqlVal = 'project= ' + project + ' AND summary ~ "\\"' + summary + '\\""'
    ticketInfo = ustocktjira.ticket_search(authenticate, jqlVal, maxresults=None)
    print(ticketInfo)
    if not ticketInfo:
        print("Ticket isnt available")
    else:
        print("Ticket found")
        ticketID = str(ticketInfo[0])
        cmmnt = "Ticket Update \n {}".format(description)
        authenticate.add_comment(ticketID,cmmnt)
        print("Comment added")

def checkIfTicketExists(host,username,token,project,summary,input,today):
    authenticate = ustocktjira.authentication(host, username, token)

    jqlVal = 'project= '+project+' AND summary ~ "\\"'+summary +'\\""'
    #print(jqlVal)
    tickets = ustocktjira.ticket_search(authenticate,jqlVal,maxresults=None)
    print(tickets)
    if not tickets:
        print("Ticket is empty")
        if input == today:
            print("Today ticket")
            return True
        else:
            print("not today ticket")
            return False
    else:
        print("Ticket list is not empty")
        return False


def returnCreatedTicketID(host, username, token, project, summary):
    authenticate = ustocktjira.authentication(host, username, token)

    jqlVal = 'project= ' + project + ' AND summary ~ "\\"{}\\""'.format(summary)
    ticketInfo = ustocktjira.ticket_search(authenticate, jqlVal, maxresults=None)
    ticketID = str(ticketInfo[0])
    print(ticketID)
    return ticketID
