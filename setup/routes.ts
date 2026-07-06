import { defineRoutesSetup } from "@slidev/types";

export default defineRoutesSetup((routes) => [
  {
    path: "/presenter/presenter/:no",
    redirect: (to) => ({
      path: `/presenter/${String(to.params.no)}`,
      query: to.query,
      hash: to.hash,
    }),
  },
  ...routes,
]);
