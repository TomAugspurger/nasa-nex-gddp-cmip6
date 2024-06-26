FROM continuumio/miniconda3 as base

COPY environment.yml ./
RUN conda update conda && \
    conda env update -f environment.yml -n base && \
    conda clean -af


FROM base as dependencies

ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /opt/stactools-nasa-nex-gddp-cmip6
COPY --from=base /opt/conda /opt/conda
COPY pyproject.toml ./
COPY src/stactools/nasa_nex_gddp_cmip6/__init__.py src/stactools/nasa_nex_gddp_cmip6/
RUN apt-get -y -q update \
    && apt-get -y -q install build-essential \
    && rm -rf /var/lib/apt/lists/
RUN python -m venv /opt/venv
RUN pip install . \
    && ls /opt/venv \
    && rm -r /opt/venv/lib/python3.11/site-packages/stactools/nasa_nex_gddp_cmip6


FROM dependencies as builder

ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /opt/stactools-nasa-nex-gddp-cmip6
COPY --from=base /opt/conda /opt/conda
COPY --from=dependencies /opt/venv /opt/venv
COPY pyproject.toml ./
COPY src ./src
RUN pip install -U pip \
    && pip install .
WORKDIR /
RUN rm -rf /opt/stactools-nasa-nex-gddp-cmip6
CMD [ "stac", "nasanexgddpcmip6" ]


FROM dependencies as dev-dependencies

ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /opt/stactools-nasa-nex-gddp-cmip6
COPY --from=dependencies /opt/venv /opt/venv
COPY pyproject.toml .
RUN pip install -e '.[dev]' \
    && git init


FROM dev-dependencies as dev-builder

ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /opt/stactools-nasa-nex-gddp-cmip6
COPY --from=base /opt/conda /opt/conda
COPY --from=dependencies /opt/venv /opt/venv
COPY . .
CMD [ "stac", "nasanexgddpcmip6" ]
