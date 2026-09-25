import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { serveStatic } from "@hono/node-server/serve-static";

const app = new Hono();

app.post("/api/feedback", (c) => {
  console.log(c.req.text());

  return c.json({ message: "Feedback received" }, 200);
});

app.use("/", serveStatic({ root: "./public" }));

serve({
  fetch: app.fetch,
  port: 3160,
  hostname: "0.0.0.0",
});
