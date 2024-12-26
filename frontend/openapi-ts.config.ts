import { defineConfig } from '@hey-api/openapi-ts';
import { defaultPlugins } from '@hey-api/openapi-ts';

export default defineConfig({
  client: '@hey-api/client-fetch',
  input: 'http://localhost:8000/openapi.json',
  output: 'src/lib/client',
  plugins: [
    ...defaultPlugins,
    {
      asClass: true,
      name: '@hey-api/sdk',
    },
  ],
});
