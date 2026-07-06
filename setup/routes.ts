type RouteLocation = {
  path: string;
  query: Record<string, unknown>;
  hash: string;
  params: Record<string, string | string[]>;
};

type RouteRedirect = {
  path: string;
  query: RouteLocation["query"];
  hash: string;
};

type RouteRecord = {
  name?: string;
  path: string;
  redirect?: (to: RouteLocation) => RouteRedirect;
  [key: string]: unknown;
};

export default (routes: RouteRecord[]): RouteRecord[] => [
  {
    path: "/presenter/presenter/:no",
    redirect: (to) => ({
      path: `/presenter/${String(to.params.no)}`,
      query: to.query,
      hash: to.hash,
    }),
  },
  ...routes,
];
