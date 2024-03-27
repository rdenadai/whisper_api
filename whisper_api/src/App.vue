<script setup>
import { watch, reactive, ref } from "vue";
import { usePermission } from "@vueuse/core";
import { useToast } from "primevue/usetoast";
import Button from "primevue/button";
import Card from "primevue/card";
import Fieldset from "primevue/fieldset";
import Toast from "primevue/toast";

const toast = useToast();
const microphoneAccess = usePermission("microphone");

const isPermissionEnabled = ref(false);
const isRecording = ref(false);

const conversation = ref({});
const chunks = reactive({ value: [] });
const mediaRecorderVue = reactive({ value: undefined });

const startRecording = async () => {
  isRecording.value = true;

  await navigator.mediaDevices
    .getUserMedia({ audio: true, video: false })
    .then((stream) => {
      const mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (event) => {
        console.log("1.here");
        chunks.value.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const formData = new FormData();
        formData.append("file", chunks.value[0]);

        isRecording.value = false;

        fetch("http://localhost:8000/upload/", {
          method: "POST",
          body: formData,
        })
          .then((response) => response.json())
          .then((data) => (conversation.value = data))
          .catch((error) =>
            toast.add({
              severity: "danger",
              summary: "Error",
              detail: `${error}`,
              life: 3000,
            }),
          );

        chunks.value = [];
      };

      mediaRecorderVue.value = mediaRecorder;
      mediaRecorder.start();
    })
    .catch((err) => {
      toast.add({
        severity: "danger",
        summary: "Error",
        detail: "Unexpected error getting microphone access",
        life: 3000,
      });
    });
};

const stopRecording = () => {
  toast.add({
    severity: "warn",
    summary: "Warn",
    detail: "Recording stopped",
    life: 3000,
  });
  mediaRecorderVue.value.stop();
};

watch(microphoneAccess, (value) => {
  if (value === "denied") {
    toast.add({
      severity: "danger",
      summary: "Error",
      detail: "Microphone access denied",
      life: 3000,
    });
  } else if (value === "granted") {
    isPermissionEnabled.value = true;
  }
});
</script>

<template>
  <div class="container">
    <Toast position="bottom-center" />
    <Card>
      <template #title>Whisper AI</template>
      <template #content>
        <p class="m-1">
          Esta é uma api simples utilizando o Whisper AI e Mixtral para que você
          possa testar o funcionamento destes modelos de IA.
        </p>

        <div class="my-3">
          <Fieldset
            class="p-2 mb-2"
            legend="Mensagem"
            v-for="message in conversation?.messages ?? []"
            :key="message.id"
          >
            <p>{{ message.text }}</p>
          </Fieldset>
        </div>
      </template>
      <template #footer>
        <div class="flex gap-4 mt-1">
          <Button
            icon="pi pi-stop-circle"
            iconPos="right"
            label="Stop"
            severity="danger"
            :disabled="!isRecording"
            style="margin-left: 0.5em"
            @click="stopRecording"
          />
          <Button
            icon="pi pi-microphone"
            iconPos="right"
            label="Record"
            :disabled="isRecording || !isPermissionEnabled"
            @click="startRecording"
          />
        </div>
      </template>
    </Card>
  </div>
</template>
