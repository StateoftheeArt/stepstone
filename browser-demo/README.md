# Browser demo, revision 2

This is the source for https://try-stepstone.corbett.chatgpt.site. It is separate from the Python account application. No learner database, real invitation or mentor credential belongs in this directory.

With Node.js 22 or newer, run `node browser-demo/build.mjs` from the repository root. Then serve `browser-demo/dist`, for example with `python -m http.server 8098 --bind 127.0.0.1 --directory browser-demo/dist`. Open http://127.0.0.1:8098/.

The build copies public lessons and assets, then applies the trial-only UI and privacy controls. It includes the public practice answer bank. Records stay on the visitor's browser; the mentor report is fictional. The trial blocks account requests, remote voices, external scripted connections, inline scripts and service workers. It does not host the full learner-and-mentor service.

Run `node check-demo.mjs` and `node check-release-security.mjs` from this directory after building. These checks cover all 144 question samplers and the trial's privacy boundaries. Browser layout and full-flow testing remain separate.

Use `?practice=release-check-120` before the route fragment for an isolated release check. Normal saved practice is preserved; the test draft and score belong to a separate local scope. No visitor data needs to be deleted.
