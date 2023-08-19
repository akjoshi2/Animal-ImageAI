import { useState } from "react";
import { createStyles, Header, Container, Group, Burger, Paper, Transition, rem} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';

interface INavBarProps
{
    links: {link: string, label: string}[];
    currIndex: number;
}

const useStyles = createStyles((theme) => ({
    header: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      height: '100%',
    },
  
    links: {
      [theme.fn.smallerThan('xs')]: {
        display: 'none',
      },
    },
  
    burger: {
      [theme.fn.largerThan('xs')]: {
        display: 'none',
      },
    },
  
    link: {
      display: 'block',
      lineHeight: 1,
      padding: `${rem(8)} ${rem(12)}`,
      borderRadius: theme.radius.sm,
      textDecoration: 'none',
      color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7],
      fontSize: theme.fontSizes.sm,
      fontWeight: 500,
  
      '&:hover': {
        backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0],
      },
    },
  
    linkActive: {
      '&, &:hover': {
        backgroundColor: theme.fn.variant({ variant: 'light', color: theme.primaryColor }).background,
        color: theme.fn.variant({ variant: 'light', color: theme.primaryColor }).color,
      },
    },
  }));

export default function NavBar(props: INavBarProps): JSX.Element
{
    const links = props.links;
    const [opened, {toggle}] = useDisclosure(false);
    const [active, setActive] = useState(links[props.currIndex].link);
    const {classes, cx} = useStyles();

    const items = links.map((link, index) => {
        return <a  
            key={link.label} 
            href={link.link}
            className={cx(classes.link, {[classes.linkActive]: active === link.link})}
            onClick={(event) => {
                setActive(link.link);
            }}
        >
            {link.label}
        </a>
    });
    

    return (
        <Header height={60}>
        <Container className={classes.header}>
            Animal-ImageAI
          <Group spacing={5} className={classes.links}>
            {items}
          </Group>
  
          <Burger opened={opened} onClick={toggle} className={classes.burger} size="sm" />
        </Container>
      </Header>
    )
}
