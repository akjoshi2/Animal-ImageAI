import { useState, useCallback } from "react";
import { Button, MantineProvider, FileInput, Text, rem } from "@mantine/core";
import { IconUpload } from "@tabler/icons-react";

export default function Animals()
{
    const [value, setValue] = useState<File | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [data, setData] = useState({animal: ""})

    function handleButtonClick() {
        setLoading(true);
        fetch("/animals").then((res) => res.json().then((resp) => {
            setData({
                animal: resp.Animal,
            });
        }));
        setLoading(false);
    }

    return (
        <MantineProvider withGlobalStyles withNormalizeCSS>
            <FileInput label = "Upload Image" placeholder="Pick file" icon={<IconUpload size={(rem(14))}/>} value={value} onChange={setValue}/>
            <Button onClick={handleButtonClick} loading={loading} loaderPosition="right">
                Predict Animal
            </Button>
            <Text>{data.animal}</Text>
        </MantineProvider>
    );
}