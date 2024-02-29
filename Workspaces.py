import boto3
from dataclasses import dataclass

LIST_WORKSPACES_PAGE_SIZE = 25


@dataclass
class WorkSpaceStruct:
    workspaceId: str = ""
    tags: str = ""
    markForDeletion: bool = False


class WorkSpacesResource:

    def _set_service(self, service='workspaces'):  # Boto3 client service
        return service

    def __init__(self) -> None:
        self.client = boto3.client(
            self._set_service(),
            region_name="us-east-1"
        )

    # Get Workspaces in an account
    def get_workspaces(self, workspaces=[]):
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
                    obj = WorkSpaceStruct()
                    obj.workspaceId = workspace['WorkspaceId']
                    workspaces.append(obj)

            self.get_workspaces_tags(workspaces=workspaces)

        except Exception as e:
            exception = True
            print(e)

        return workspaces, exception

    # Fetch tags against each workspace from service-end since the describe-workspaces doesn't return tags
    def get_workspaces_tags(self, workspaces=[]):
        try:
            for workspace in workspaces:
                response = self.client.describe_tags(
                    ResourceId=workspace.workspaceId
                )
                responseTags = response["TagList"]
                workspace.tags = response["TagList"]
                deleteTag = list(
                    filter(lambda responseTags: responseTags['Key'] == 'auto-delete', responseTags))
                workspace.markForDeletion = True if len(
                    deleteTag) > 0 and deleteTag[0]['Value'] != 'no' else False
                print(workspaces)
        except Exception as e:
            print(e)

    def delete(self, resource):
        response = self.client.terminate_workspaces(
            TerminateWorkspaceRequests=[
                {
                    'WorkspaceId': 'string'
                },
            ]
        )


obj = WorkSpacesResource()
obj.get_workspaces()
