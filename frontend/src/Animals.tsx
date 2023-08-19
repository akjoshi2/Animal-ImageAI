import { useState, useCallback } from "react";
import { Button, MantineProvider, FileInput, Text, rem, Box, Group, Header, Container, createStyles, Center } from "@mantine/core";
import { useForm } from "@mantine/form";
import { IconUpload } from "@tabler/icons-react";
import axios from "axios";
import NavBar from "./NavBar";

const animalStyles = createStyles((theme) => ({
    box: {
        padding: theme.spacing.xl,
        borderRadius: theme.radius.md,
    },
    button: {
        marginTop: '10px',
    }
}));

export default function Animals(): JSX.Element
{
    const { classes } = animalStyles();
    const [value, setValue] = useState<File | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [data, setData] = useState({animal: ""})
    const links = [{label: "Main", link: "http://localhost:3000/"}, {label: "Dogs", link: "http://localhost:3000/dogs"}]

    const form = useForm({
        initialValues: {
            image: value
        }
    })

    function handleButtonClick() {
        if (value !== null)
        {
            setLoading(true);
            let formData = new FormData()
            formData.append('image',value);
            axios({
                    url: '/animals',
                    method: 'POST',
                    data: formData,
            }).then((resp) => {
                setData({
                    animal: resp.data.Animal,
                })
                setLoading(false);
            });
        }
    }

    function handleFormSubmit(image: File | null) {
        if (image !== null)
        {
            setLoading(true);
            let formData = new FormData()
            formData.append('image',image);
            axios({
                    url: '/animals',
                    method: 'POST',
                    data: formData,
            }).then((resp) => {
                setData({
                    animal: resp.data.Animal,
                })
                setLoading(false);
            });
        }
    }

    return (
        <MantineProvider withGlobalStyles withNormalizeCSS>
            {/*<FileInput label = "Upload Image" placeholder="Pick file" icon={<IconUpload size={(rem(14))}/>} value={value} onChange={setValue}/>
            <Button onClick={handleButtonClick} loading={loading} loaderPosition="right">
                Predict Animal
            </Button>*/
            }
            <NavBar links={links} currIndex={0} />
            <Box maw={500} className={classes.box}>
                <form onSubmit={form.onSubmit((values) => handleFormSubmit(values.image))}>
                <FileInput label = "Upload Image" placeholder="Pick file" icon={<IconUpload size={(rem(14))}/>} {...form.getInputProps('image')}/>
                <Group>
                    <Button type="submit" onClick={handleButtonClick} loading={loading} loaderPosition="right" className={classes.button}>
                    Predict Animal
                    </Button>
                </Group>
                </form>
                <Text size={rem(75)}>{data.animal}</Text>
            </Box>

        </MantineProvider>
    );
}