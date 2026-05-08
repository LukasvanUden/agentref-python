from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from .._http import AsyncHttpClient, SyncHttpClient

_MERCHANT_KIND = Literal["all", "collections", "files", "social_posts", "swipe_copy", "links", "drafts"]
_AFFILIATE_KIND = Literal["all", "collections", "files", "social_posts", "swipe_copy", "links"]
_RESOURCE_STATUS = Literal["published", "draft", "archived"]
_PLATFORM = Literal["x", "linkedin", "instagram", "tiktok", "facebook", "threads", "generic"]
_BUNDLE = Literal["social_post_media", "collection_files"]


def _data_dict(envelope: Dict[str, Any]) -> Dict[str, Any]:
    data = envelope.get("data", {})
    return data if isinstance(data, dict) else {}


def _data_list(envelope: Dict[str, Any]) -> List[Dict[str, Any]]:
    data = envelope.get("data", [])
    return [item for item in data if isinstance(item, dict)] if isinstance(data, list) else []


class MarketingResourcesResource:
    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(
        self,
        program_id: str,
        *,
        kind: Optional[_MERCHANT_KIND] = None,
        status: Optional[_RESOURCE_STATUS] = None,
        search: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        envelope = self._http.request(
            "GET",
            f"/programs/{program_id}/marketing-resources",
            params={"kind": kind, "status": status, "search": search, "limit": limit, "offset": offset},
        )
        return _data_list(envelope)

    def create_social_post(
        self,
        program_id: str,
        *,
        title: str,
        body: str,
        platforms: List[_PLATFORM],
        description: Optional[str] = None,
        instructions: Optional[str] = None,
        collection_id: Optional[str] = None,
        folder_id: Optional[str] = None,
        status: Optional[Literal["draft", "published"]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "title": title,
            "description": description,
            "body": body,
            "platforms": platforms,
            "instructions": instructions,
            "collection_id": collection_id,
            "folder_id": folder_id,
            "status": status,
        }
        envelope = self._http.request(
            "POST",
            f"/programs/{program_id}/marketing-resources/social-posts",
            json={k: v for k, v in payload.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    def update_social_post(
        self,
        resource_id: str,
        *,
        program_id: str,
        title: Optional[str] = None,
        body: Optional[str] = None,
        platforms: Optional[List[_PLATFORM]] = None,
        description: Optional[str] = None,
        instructions: Optional[str] = None,
        collection_id: Optional[str] = None,
        folder_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "program_id": program_id,
            "title": title,
            "description": description,
            "body": body,
            "platforms": platforms,
            "instructions": instructions,
            "collection_id": collection_id,
            "folder_id": folder_id,
        }
        envelope = self._http.request(
            "PATCH",
            f"/marketing-resources/social-posts/{resource_id}",
            json={k: v for k, v in payload.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    def create_social_post_media_upload_session(
        self,
        resource_id: str,
        *,
        program_id: str,
        file_name: str,
        mime_type: str,
        file_size_bytes: int,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        envelope = self._http.request(
            "POST",
            f"/marketing-resources/social-posts/{resource_id}/media/upload-sessions",
            json={
                "program_id": program_id,
                "file_name": file_name,
                "mime_type": mime_type,
                "file_size_bytes": file_size_bytes,
            },
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    def complete_social_post_media_upload(
        self,
        resource_id: str,
        *,
        program_id: str,
        upload_path: str,
        upload_token: str,
        file_name: str,
        alt_text: Optional[str] = None,
        sort_order: Optional[int] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self._media_upload_mutation(
            f"/marketing-resources/social-posts/{resource_id}/media/complete",
            program_id=program_id,
            upload_path=upload_path,
            upload_token=upload_token,
            file_name=file_name,
            alt_text=alt_text,
            sort_order=sort_order,
            idempotency_key=idempotency_key,
        )

    def reorder_social_post_media(
        self,
        resource_id: str,
        *,
        program_id: str,
        media_ids: List[str],
        idempotency_key: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        envelope = self._http.request(
            "POST",
            f"/marketing-resources/social-posts/{resource_id}/media/reorder",
            json={"program_id": program_id, "media_ids": media_ids},
            idempotency_key=idempotency_key,
        )
        return _data_list(envelope)

    def update_social_post_media(
        self,
        resource_id: str,
        media_id: str,
        *,
        program_id: str,
        alt_text: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        envelope = self._http.request(
            "PATCH",
            f"/marketing-resources/social-posts/{resource_id}/media/{media_id}",
            json={"program_id": program_id, "alt_text": alt_text},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    def remove_social_post_media(
        self,
        resource_id: str,
        media_id: str,
        *,
        program_id: str,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        envelope = self._http.request(
            "DELETE",
            f"/marketing-resources/social-posts/{resource_id}/media/{media_id}",
            json={"program_id": program_id},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    def replace_social_post_media(
        self,
        resource_id: str,
        media_id: str,
        *,
        program_id: str,
        upload_path: str,
        upload_token: str,
        file_name: str,
        alt_text: Optional[str] = None,
        sort_order: Optional[int] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self._media_upload_mutation(
            f"/marketing-resources/social-posts/{resource_id}/media/{media_id}/replace",
            program_id=program_id,
            upload_path=upload_path,
            upload_token=upload_token,
            file_name=file_name,
            alt_text=alt_text,
            sort_order=sort_order,
            idempotency_key=idempotency_key,
        )

    def publish(
        self,
        resource_id: str,
        *,
        program_id: str,
        notify_affiliates: Optional[bool] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        envelope = self._http.request(
            "POST",
            f"/marketing-resources/{resource_id}/publish",
            json={"program_id": program_id, "notify_affiliates": notify_affiliates},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    def unpublish(self, resource_id: str, *, program_id: str, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        return self._status_mutation(resource_id, "unpublish", program_id=program_id, idempotency_key=idempotency_key)

    def archive(self, resource_id: str, *, program_id: str, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        return self._status_mutation(resource_id, "archive", program_id=program_id, idempotency_key=idempotency_key)

    def notify_affiliates(
        self,
        resource_id: str,
        *,
        program_id: str,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        envelope = self._http.request(
            "POST",
            f"/marketing-resources/{resource_id}/notify",
            json={"program_id": program_id},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    def create_download_url(
        self,
        *,
        program_id: str,
        media_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        collection_id: Optional[str] = None,
        bundle: Optional[_BUNDLE] = None,
        file: Optional[Literal[True]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "program_id": program_id,
            "media_id": media_id,
            "resource_id": resource_id,
            "collection_id": collection_id,
            "bundle": bundle,
            "file": file,
        }
        envelope = self._http.request(
            "POST",
            "/marketing-resources/download-url",
            json={k: v for k, v in payload.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    def list_for_affiliate(
        self,
        program_id: str,
        *,
        kind: Optional[_AFFILIATE_KIND] = None,
        search: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        envelope = self._http.request(
            "GET",
            f"/me/programs/{program_id}/marketing-resources",
            params={"kind": kind, "search": search, "limit": limit, "offset": offset},
        )
        return _data_list(envelope)

    def get_for_affiliate(self, resource_id: str, *, program_id: str) -> Dict[str, Any]:
        envelope = self._http.request(
            "GET",
            f"/me/marketing-resources/{resource_id}",
            params={"program_id": program_id},
        )
        return _data_dict(envelope)

    def create_affiliate_download_url(
        self,
        *,
        program_id: str,
        media_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        collection_id: Optional[str] = None,
        bundle: Optional[_BUNDLE] = None,
        file: Optional[Literal[True]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "program_id": program_id,
            "media_id": media_id,
            "resource_id": resource_id,
            "collection_id": collection_id,
            "bundle": bundle,
            "file": file,
        }
        envelope = self._http.request(
            "POST",
            "/me/marketing-resources/download-url",
            json={k: v for k, v in payload.items() if v is not None},
        )
        return _data_dict(envelope)

    def render_social_post(
        self,
        resource_id: str,
        *,
        program_id: str,
        affiliate_link_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        envelope = self._http.request(
            "POST",
            f"/me/marketing-resources/social-posts/{resource_id}/render",
            json={"program_id": program_id, "affiliate_link_id": affiliate_link_id},
        )
        return _data_dict(envelope)

    def _media_upload_mutation(
        self,
        path: str,
        *,
        program_id: str,
        upload_path: str,
        upload_token: str,
        file_name: str,
        alt_text: Optional[str],
        sort_order: Optional[int],
        idempotency_key: Optional[str],
    ) -> Dict[str, Any]:
        payload = {
            "program_id": program_id,
            "upload_path": upload_path,
            "upload_token": upload_token,
            "file_name": file_name,
            "alt_text": alt_text,
            "sort_order": sort_order,
        }
        envelope = self._http.request(
            "POST",
            path,
            json={k: v for k, v in payload.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    def _status_mutation(
        self,
        resource_id: str,
        action: Literal["unpublish", "archive"],
        *,
        program_id: str,
        idempotency_key: Optional[str],
    ) -> Dict[str, Any]:
        envelope = self._http.request(
            "POST",
            f"/marketing-resources/{resource_id}/{action}",
            json={"program_id": program_id},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)


class AsyncMarketingResourcesResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self, program_id: str, **kwargs: Any) -> List[Dict[str, Any]]:
        return await _run_async(self._http, "GET", f"/programs/{program_id}/marketing-resources", params=kwargs)

    async def create_social_post(
        self,
        program_id: str,
        *,
        title: str,
        body: str,
        platforms: List[_PLATFORM],
        description: Optional[str] = None,
        instructions: Optional[str] = None,
        collection_id: Optional[str] = None,
        folder_id: Optional[str] = None,
        status: Optional[Literal["draft", "published"]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "title": title,
            "description": description,
            "body": body,
            "platforms": platforms,
            "instructions": instructions,
            "collection_id": collection_id,
            "folder_id": folder_id,
            "status": status,
        }
        envelope = await self._http.request(
            "POST",
            f"/programs/{program_id}/marketing-resources/social-posts",
            json={k: v for k, v in payload.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    async def update_social_post(self, resource_id: str, **kwargs: Any) -> Dict[str, Any]:
        idempotency_key = kwargs.pop("idempotency_key", None)
        envelope = await self._http.request(
            "PATCH",
            f"/marketing-resources/social-posts/{resource_id}",
            json={k: v for k, v in kwargs.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    async def create_social_post_media_upload_session(self, resource_id: str, **kwargs: Any) -> Dict[str, Any]:
        idempotency_key = kwargs.pop("idempotency_key", None)
        envelope = await self._http.request(
            "POST",
            f"/marketing-resources/social-posts/{resource_id}/media/upload-sessions",
            json={k: v for k, v in kwargs.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    async def complete_social_post_media_upload(self, resource_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._post_dict(f"/marketing-resources/social-posts/{resource_id}/media/complete", kwargs)

    async def reorder_social_post_media(self, resource_id: str, **kwargs: Any) -> List[Dict[str, Any]]:
        envelope = await self._post_envelope(f"/marketing-resources/social-posts/{resource_id}/media/reorder", kwargs)
        return _data_list(envelope)

    async def update_social_post_media(self, resource_id: str, media_id: str, **kwargs: Any) -> Dict[str, Any]:
        idempotency_key = kwargs.pop("idempotency_key", None)
        envelope = await self._http.request(
            "PATCH",
            f"/marketing-resources/social-posts/{resource_id}/media/{media_id}",
            json={k: v for k, v in kwargs.items() if v is not None},
            idempotency_key=idempotency_key,
        )
        return _data_dict(envelope)

    async def remove_social_post_media(self, resource_id: str, media_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._post_dict(f"/marketing-resources/social-posts/{resource_id}/media/{media_id}", kwargs, method="DELETE")

    async def replace_social_post_media(self, resource_id: str, media_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._post_dict(f"/marketing-resources/social-posts/{resource_id}/media/{media_id}/replace", kwargs)

    async def publish(self, resource_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._post_dict(f"/marketing-resources/{resource_id}/publish", kwargs)

    async def unpublish(self, resource_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._post_dict(f"/marketing-resources/{resource_id}/unpublish", kwargs)

    async def archive(self, resource_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._post_dict(f"/marketing-resources/{resource_id}/archive", kwargs)

    async def notify_affiliates(self, resource_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._post_dict(f"/marketing-resources/{resource_id}/notify", kwargs)

    async def create_download_url(self, **kwargs: Any) -> Dict[str, Any]:
        return await self._post_dict("/marketing-resources/download-url", kwargs)

    async def list_for_affiliate(self, program_id: str, **kwargs: Any) -> List[Dict[str, Any]]:
        return await _run_async(self._http, "GET", f"/me/programs/{program_id}/marketing-resources", params=kwargs)

    async def get_for_affiliate(self, resource_id: str, *, program_id: str) -> Dict[str, Any]:
        envelope = await self._http.request(
            "GET",
            f"/me/marketing-resources/{resource_id}",
            params={"program_id": program_id},
        )
        return _data_dict(envelope)

    async def create_affiliate_download_url(self, **kwargs: Any) -> Dict[str, Any]:
        return await self._post_dict("/me/marketing-resources/download-url", kwargs)

    async def render_social_post(self, resource_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._post_dict(f"/me/marketing-resources/social-posts/{resource_id}/render", kwargs)

    async def _post_envelope(self, path: str, payload: Dict[str, Any], *, method: str = "POST") -> Dict[str, Any]:
        idempotency_key = payload.pop("idempotency_key", None)
        return await self._http.request(
            method,
            path,
            json={k: v for k, v in payload.items() if v is not None},
            idempotency_key=idempotency_key,
        )

    async def _post_dict(self, path: str, payload: Dict[str, Any], *, method: str = "POST") -> Dict[str, Any]:
        return _data_dict(await self._post_envelope(path, payload, method=method))


async def _run_async(
    http: AsyncHttpClient,
    method: str,
    path: str,
    *,
    params: Dict[str, Any],
) -> List[Dict[str, Any]]:
    envelope = await http.request(method, path, params={k: v for k, v in params.items() if v is not None})
    return _data_list(envelope)
