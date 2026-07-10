const normalizeSlidevHash = () => {
  const normalized = window.location.hash
    .replace(/^#\/self-seminar-measure-theory(?=\/|$)/, "#")
    .replace(/^#\/presenter\/presenter\//, "#/presenter/");

  if (normalized !== window.location.hash) {
    window.location.hash = normalized.slice(1);
  }
};

const scheduleHashNormalization = () => {
  normalizeSlidevHash();
  window.setTimeout(normalizeSlidevHash, 0);
  window.setTimeout(normalizeSlidevHash, 100);
  window.setTimeout(normalizeSlidevHash, 500);
  window.setTimeout(normalizeSlidevHash, 1000);
};

export default () => {
  scheduleHashNormalization();
  window.addEventListener("hashchange", scheduleHashNormalization);
  window.setInterval(normalizeSlidevHash, 250);
};
