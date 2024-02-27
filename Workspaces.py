import boto3

LIST_WORKSPACES_PAGE_SIZE = 25


class WorkSpacesResource:

    def _set_service(self, service='workspaces'):  # Boto3 client service
        return service

    def __init__(self) -> None:
        self.client = boto3.client(
            self._set_service(),
            region_name="us-east-1"
        )
        print("Zeeshan")

    # Get Workspaces in an account
    def get_workspaces(self, tags=[], workspaceIds=[]):
        exception = False
        try:
            paginator = self.client.get_paginator('describe_workspaces')
            response_iterator = paginator.paginate(
                PaginationConfig={
                    'Limit': LIST_WORKSPACES_PAGE_SIZE
                }
            )

            for page in response_iterator:
                for workspace in page['Workspaces']:
                    workspaceIds.append(workspace['WorkspaceId'])

            self.get_workspaces_tags(workspacesIds=workspaceIds)

        except Exception as e:
            exception = True
            print(e)

        return tags, exception

    # Fetch tags against each workspace
    def get_workspaces_tags(self, workspacesIds=[]):
        try:
            for workspace in workspacesIds:
                response = self.client.describe_tags(
                    ResourceId=workspace
                )
                print(response)
        except Exception as e:
            print(e)

        print("Hello I am here")


obj = WorkSpacesResource()
obj.get_workspaces()
