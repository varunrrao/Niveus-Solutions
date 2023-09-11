import google.cloud.dlp
def redact_image(
    project: str,
    filename: str,
    output_filename: str,
    info_types: list[str],
    min_likelihood: str = None,
) -> None:
    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    info_types = [{"name": info_type} for info_type in info_types]

    # Prepare image_redaction_configs, a list of dictionaries. Each dictionary
    # contains an info_type and optionally the color used for the replacement.
    # The color is omitted in this sample, so the default (black) will be used.
    image_redaction_configs = []

    if info_types is not None:
        for info_type in info_types:
            image_redaction_configs.append({"info_type": info_type})

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        "min_likelihood": min_likelihood,
        "info_types": info_types,
    }
    # Construct the byte_item, containing the file's byte data.
    with open(filename, mode="rb") as f:
        byte_item = {"type_": "IMAGE", "data": f.read()}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.redact_image(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "image_redaction_configs": image_redaction_configs,
            "byte_item": byte_item,
        }
    )

    # Write out the results.
    with open(output_filename, mode="wb") as f:
        f.write(response.redacted_image)
    print(
        "Wrote {byte_count} bytes to {filename}".format(
            byte_count=len(response.redacted_image), filename=output_filename
        )
    )
redact_image("presales-286307",'uid_image.jpg','a4.jpg',["INDIA_AADHAAR_INDIVIDUAL"],"POSSIBLE")