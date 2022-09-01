const manifest = self.__WB_MANIFEST;
if (manifest) {
  // do nothing
}

// https://web.dev/offline-fallback-page/
const CACHE_NAME = "offline-html";
const FALLBACK_HTML_URL = "/offline/";
self.addEventListener("install", (event) => {
  event.waitUntil(
    // Setting {cache: 'reload'} in the new request will ensure that the
    // response isn't fulfilled from the HTTP cache; i.e., it will be from
    // the network.
    caches
      .open(CACHE_NAME)
      .then((cache) =>
        cache.add(new Request(FALLBACK_HTML_URL, { cache: "reload" }))
      )
  );

  // Force the waiting service worker to become the active service worker.
  self.skipWaiting();
});

self.addEventListener("activate", function (event) {
  // Tell the active service worker to take control of the page immediately.
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches
      .match(event.request)
      .then((response) => {
        return response || fetch(event.request);
      })
      .catch(() => {
        return caches.match(FALLBACK_HTML_URL);
      })
  );
});
