FROM alpine:edge as meshery-server
ADD . .

FROM alpine:edge
COPY --from=meshery-server /Makefile /app/cmd/
WORKDIR /app/cmd
CMD ["make", "--help"]
