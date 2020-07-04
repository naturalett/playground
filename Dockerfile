FROM alpine:edge as meshery-server
ADD . .

FROM alpine:edge
COPY --from=meshery-server /Makefile /home/
CMD ["make", "--help"]
