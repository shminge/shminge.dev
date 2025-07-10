import React from 'react';

export interface LinkWidgetProps {
  icon: string;
  backgroundColour: string;
  link: string;
  altText: string;
}

const LinkWidget: React.FC<LinkWidgetProps> = ({ icon, backgroundColour, link, altText }) => {
  return (
    <div
      className="rounded-lg w-16 h-16 flex items-center justify-center" // make it small and square
      style={{ backgroundColor: backgroundColour }}
    >
      <a href={link}>
        <img
          src={icon}
          alt={altText}
          className="w-10 h-10 object-cover" // keep the image square
        />
      </a>
    </div>
  );
}

export default LinkWidget;
