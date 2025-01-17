import { Avatar, IconButton, Link, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import CloseIcon from "@material-ui/icons/Close";
import React, { useContext } from "react";
import { getLocalePrefix } from "../../../public/lib/apiOperations";
import getTexts from "../../../public/texts/texts";
import UserContext from "../context/UserContext";
import { getImageUrl } from "./../../../public/lib/imageOperations";
import Truncate from "react-truncate";

const useStyles = makeStyles((theme) => ({
  orgName: {
    display: "inline-block",
    wordBreak: "break-word",
  },
  smallAvatar: (props) => ({
    height: 20,
    width: 20,
    border: props.showBorder && "0.5px solid gray",
  }),
  mediumAvatar: (props) => ({
    height: 30,
    width: 30,
    border: props.showBorder && "0.5px solid gray",
  }),
  avatarWrapper: {
    display: "inline-block",
    verticalAlign: "middle",
    marginRight: theme.spacing(1),
    wordBreak: "break-word",
  },
  wrapper: {
    display: "inline-flex",
    alignItems: "center",
  },
  mediumOrgName: {
    fontSize: 16,
    wordBreak: "break-word",
  },
}));

export default function MiniOrganizationPreview({
  organization,
  className,
  size,
  onDelete,
  nolink,
  doNotShowName,
}) {
  const { locale } = useContext(UserContext);
  if (!nolink)
    return (
      <Link
        className={className}
        color="inherit"
        href={getLocalePrefix(locale) + "/organizations/" + organization.url_slug}
        target="_blank"
      >
        <Content
          organization={organization}
          size={size}
          onDelete={onDelete}
          doNotShowName={doNotShowName}
        />
      </Link>
    );
  else
    return (
      <div className={className}>
        <Content
          organization={organization}
          size={size}
          onDelete={onDelete}
          doNotShowName={doNotShowName}
        />
      </div>
    );
}

function Content({ organization, size, onDelete, doNotShowName }) {
  const { locale } = useContext(UserContext);
  const texts = getTexts({ page: "organization", locale: locale, organization: organization });
  const classes = useStyles({ showBorder: doNotShowName });
  const avatarProps = {
    alt: texts.organizations_logo,
    src: getImageUrl(organization.thumbnail_image),
    className: `${size === "small" && classes.smallAvatar} ${
      size === "medium" && classes.mediumAvatar
    }`,
  };
  return (
    <span className={classes.wrapper}>
      <div className={classes.avatarWrapper}>
        <Avatar {...avatarProps} />
      </div>
      {!doNotShowName && (
        <>
          {size === "small" ? (
            <Truncate lines={2}>
              <Typography>{organization.name}</Typography>
            </Truncate>
          ) : size === "medium" ? (
            <Typography className={classes.mediumOrgName}>{organization.name}</Typography>
          ) : (
            <Typography variant="h5" className={classes.orgName}>
              {organization.name}
            </Typography>
          )}
          {onDelete && (
            <IconButton onClick={() => onDelete(organization)}>
              <CloseIcon />
            </IconButton>
          )}
        </>
      )}
    </span>
  );
}
