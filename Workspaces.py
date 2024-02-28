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

            self.get_workspaces_tags(workspacesIds=workspaceIds, tags=tags)

        except Exception as e:
            exception = True
            print(e)

        return tags, exception

    # Fetch tags against each workspace from service-end since the describe-workspaces doesn't return tags
    def get_workspaces_tags(self, workspacesIds=[], tags=[]):
        try:
            for workspace in workspacesIds:
                response = self.client.describe_tags(
                    ResourceId=workspace
                )
                responseTags = response["TagList"]
                obj = WorkSpaceStruct()
                obj.workspaceId = workspace
                obj.tags = response["TagList"]
                deleteTag = list(
                    filter(lambda responseTags: responseTags['Key'] == 'auto-delete', responseTags))
                obj.markForDeletion = True if len(
                    deleteTag) > 0 and deleteTag[0]['Value'] != 'no' else False
                tags.append(obj)
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
